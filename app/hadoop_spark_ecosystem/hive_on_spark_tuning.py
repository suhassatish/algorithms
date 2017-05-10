"""
https://cwiki.apache.org/confluence/display/Hive/Hive+on+Spark
Hive-on-spark design document
Map-reduce's in-built shuffle capability has the following equivalent transformations in spark -
a) partitionBy - does pure shuffling (no grouping or sorting)
b) groupByKey - does shuffling and grouping
c) sortByKey - does shuffling and sorting

1) Hive query is broken down using an abstract syntax tree of logical operators in a plan.

2) Some of these are TableScanOperator, FileSinkOperator, ReduceSink, GroupByOperator,
MapJoinOperator.

3) MapReduceCompiler converts the logical operator plan to a graph (DAG) of MapReduceTasks &
MoveTasks

4) Similarly SparkCompiler converts the logical plan into a SparkTask, a unit of work of a spark job
 SparkWork describes the plan of a SparkTask.

  a) SparkCompiler is also responsible for physical optimizations on spark.

  b) Internally, SparkTask.execute() will make RDDs & functions out of a SparkWork instance & submit
   it to a spark cluster for execution via a SparkClient.

  c) MapFunction and ReduceFunction are built from SparkWork and applied to transform RDDs

  d) Job execution is triggered by applying a foreach() TX on the RDDs with a dummy function

5) Right design choice is 1 SparkContext per user session, but in spark 1.2 there was 1 SparkContext
per application because of some thread safety issues.

6) All map function and reduce function has to be serializable as its shipped to the cluster.

7) Hive operators have to be initialized with operator.init(), then operator.process() needs to be
called, then operator.close(). But spark operators are functional. Spark's MapFunction() and
ReduceFunction() will have to perform all those in a single call() function.

8) mapPartitions transformation operator on RDDs provides an iterator on a whole partition of data.

9) Hive's groupBy doesnt expect the keys to be sorted but map-reduce does it anyway. Spark gives
you flexibility with partitionBy, groupByKey or sortByKey transformations.
--------------------------------------------------------------------------
KEY DIFFERENCES BETWEEN MAP-REDUCE AND SPARK -
1) An executor JVM in spark can process from multiple different HDFS splits. This is a deviation
 from map-reduce where a map task JVM always reads from the same HDFS split.

2) In the map-reduce world, map-side operator tree and reduce-side operator tree run as single
threads in map-reduce within an isolated JVM. But in spark, the operator tree can be reused within
a shared JVM. This could potentially cause concurrency and thread safety issues, with static
variables and the like.

3) In the map-reduce world, ExecMapper.done is polled to terminate a MapTask JVM. But in spark, if
2 ExecMappers share the same JVM, the 1 that completes 1st could terminate the JVM before the other
finishes.

--------------------------------------------------------------------------
https://cwiki.apache.org/confluence/display/Hive/Hive+on+Spark%3A+Join+Design+Master
Hive on Spark: Join Design Master
Look at Szehon Ho's visual color-coded Class pipeline diagram - its too complicated to describe
Following use cases are starting points - all OPTIMIZERS operate on Logical plans, RESOLVERS operate
on physical plans

1) Tables are skewed:
    a) SkewJoinResolver (hive.optimize.skew.join)
    b) MapJoinResolver (if contains MapWork or MapLocalWork)

2) Tables are skewed and skew metadata is available
    a) SkewJoinOptimizer (hive.optimize.skewjoin.compiletime)
    b) CommonJoinResolver (hive.auto.convert.join)
    c) MapJoinResolver (if contains MapWork or MapLocalWork)

3) N -1 join tables fit in memory

4) User provides join hints
5) User provides join hints and tables are bucketed
6) User provides join hints and tables are bucketed & sorted
7) Tables bucketed and sorted
--------------------------------------------------------------------------
TUNING HIVE ON SPARK
https://www.cloudera.com/documentation/enterprise/5-9-x/topics/admin_hos_tuning.html

In a yarn cluster, lets say each worker machine has 32 cores and 120 GB RAM. Usually, the only
services that run on each worker node are NodeManager service and HDFS DataNode service.
If you leave 2 cores for OS usage and 1 core for each of the above services, it leaves 28 cores
available for YARN.

CONFIGURING MEMORY -
Allocate 20 GB memory to the 2 services (10 GB each). Make the other 100 GB
available to YARN by setting the following properties -
yarn.nodemanager.resource.memory-mb = 100 GB
yarn.nodemanager.resource.cpu-vcores = 28
------------------------------
4 KEY TUNING PARAMETERS IN SPARK -
1) EXECUTOR MEMORY -
  a) More memory means more map-join optimizations, but greater garbage collection
overhead.
  b) HDFS doesnt handle concurrent writers well, so there could be race conditions if multiple
cores are used by an executor.

  c) Recommended setting is spark.executor.cores = 4,5 or 6, depending on number of cores allocated
to YARN. If yarn has total 28 cores, then make spark.executor.cores = 4 so that total 7 executors
can run in parallel on a machine. If spark.executor.cores = 5, then u can run 5 executors in
parallel and 3 cores will be unused.

  d) Now divide up total node manager memory equally among all executors. So 100/7 ~ 14 GB mem per
   executor. Total memory YARN can use to create an executor JVM process =
   spark.executor.memory + spark.yarn.executor.memoryOverhead (keep about 15-20% of total for this)
  = 12 GB + 2 GB (recommended for 14 GB in above calculations)

2) DRIVER MEMORY - Total memory YARN can use to create a driver Process =
spark.driver.memory (max size of each spark driver's java heap memory)
+ spark.yarn.driver.memoryOverhead (extra off-heap memory that can be requested from yarn, per
driver)
If X = yarn.nodemanager.resource.memory-mb, thumb rule is roughly 25% of that = driver memory;
ie, if X = 50 GB, driver memory = 12 GB; 10.5 GB heap + 1.5 GB off-heap

3) NUMBER OF EXECUTORS - Query performance for hive-on-spark is directly proportional to the
number of executors. In a 40 node cluster, max number of executors = 40 * 4 = 160; But little less
than this in reality as driver takes up some cores and memory. Thumb rule - For max performance,
use all available executors. In typical production scenario, try to use 50% of cluster capacity for
number of executors.

4) PARALLELISM -
    a) Number of map tasks = number of splits generated by input format
    b) hive.exec.reducers.bytes.per.reducer controls how much data each reducer handles
    c) Based on b), # of executors, executor memory and other factors, hive generates the optimal
    number of partitions (which determines the number of reduce tasks) to keep all executors busy.
----------------------------------------
DYNAMIC ALLOCATION -
This allows the executors from an application to be reused by other applications, once its no
longer needed by the 1st application. If True, the 1st application will try to hog all resources
and spawn as many executors. All other applications will be queued. To prevent starvation, create
pooled queues, using Yarn fair scheduler.

PRE-WARMING YARN CONTAINERS -
1) Once client issues spark-submit, Spark doesnt wait for all executors to start before starting the
jobs.
2) 1st time latency is more to start executors, subsequently they're fast.
3) The number of available executors at the time of job submission partly determines the number of
reducers.
4) Due to the above, for short-lived sessions like hive-on-spark launched by oozie, this long 1st
time latency can be problematic. Hence use container pre-warming to offset this.  In this case,
the job starts running only when all the requested executors are ready. This way, a short-lived
session's parallelism is not decreased on the reducer side.


"""