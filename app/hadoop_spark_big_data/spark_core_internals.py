# -*- coding: utf-8 -*-
"""
https://github.com/JerryLead/SparkInternals/blob/master/EnglishVersion/2-JobLogicalPlan.md
Spark Logical Plan -
1) `transformation()` decides what kind of RDD is produced. Some TX are reused by other operations,
eg `cogroup`

2) Depdendency of an RDD depends on the semantics of the Tx.
eg - `CoGroupRDD` depends on all RDDs used for cogroup

3) RDD partitions can have a `NarrowDependency` (full dependency eg- 1:1 dependency and RangeDep)
or a `ShuffleDependency`(partial dependency, ie each child depdens on a part of the parent
partition).

A dependency is a narrow dependency if the RDD's number of partitions & partitioner type are the
same.

4) MapReduce dataflow is equivalent to map() + reduceByKey().
------------------------------------------------------------------------------------------------
RDDs can be cached in-memory or persisted on disk by calling cache(), persist() or checkpoint()
Number of partitions is usually set by the user.

eg - val x = a.join(b)
If a is an RDD of m partitions and b is an RDD of n partitions, x will have max(M,N) partitions
------------------------------------------------------------------------------------------------
https://github.com/JerryLead/SparkInternals/blob/master/EnglishVersion/2-JobLogicalPlan.md
great charts with example illustrations of key-value pairs

DETAILS OF SOME OPERATIONS & TRANSFORMATIONS UNDER THE HOOD -

1)
groupByKey(numPartitions) - sequence of operations
creates -> ShuffledRDD -> compute() function fetches necessary data for its partitions
-> mapPartition() fn in 1:1 Dep style -> MapPartitionsRDD -> ArrayBuffer of values is casted to
 iterable.
  a) groupByKey() has no map-side combine as it does not reduce the amt of data shuffled & requires
   map-side data be inserted into a hash table, leading to too many objects in OldGen GC objects

  b) ArrayBuffer is essentially a `CompactBuffer` but is append-only and more memory-efficient for
  small buffers.

2)
reduceByKey(func, numPartitions) - sequence of operations
  a) Enables map-side combine by default, its carried out by mapPartitions()
  b) ParallelCollectionsRDD -> MapPartitionsRDD -> ShuffledRDD -> MapPartitionsRDD

3)
distinct(numPartitions) - it calls reduceByKey() under the hood which has to shuffle. For shuffle,
RDD has to be of the type RDD(K,V). So an RDD[Int] is map() to RDD[Int, Null] .

ParallelCollectionRDD ->   MappedRDD    -> MapPartitionsRDD -> ShuffledRDD -> MapPartitionsRDD -> map() -> MappedRDD
    RDD[Int]             RDD[Int, Null]                                                              null values thrown away

4) cogroup(otherRDD, numPartitions) - eg a.cogroup(b, numPartitions = 4)
    a) Type of partitioner (HashPartitioner by default)determines how to partition the data

------------------------------------------------------------------------------------------------

METHODS DECLARED ON RDDs -

1) getDependency() - this declares data dependency of each RDD (its parents).
dependency.getParents() method gets the dependent partitions

2) compute() - Receives upstream records (from parentRDD or data source) and applies computation
   The compute() method returns an iterator of the computed records in the RDD for next computation
Internally, the compute method implementation looks like the below example -
firstParent[T].iterator(split, context).map(f)
Records in the first parent dependent RDD, are iterated over one by one and map(f) is applied.

3) processPartition() method - Defines how to process the records in each partition and generate the
partial result of finalRDD

4) resultHandler() method - Defines how to process partial results from each partition to form the
final results.

5) Actions - These are in user's driver program. eg - reduce(func), count(), collect(), foreach(f),
take(n), first(), takeSample(), takeOrdered(n, [ordering]), saveAsHadoopFile(path), countByKey()

We will have as many `JOBS` submitted as there are actions in the driver program.
For eg, the foreach() action will call sc.runJob(this, (iter: Iterator[T])) => iter.foreach(f)
The job is submitted to the DAGScheduler. The DAGScheduler applies the Application-LogicalPlan-
PhysicalPlan strategy to figure out the stages, and submits firstly the stages without parents for
execution. In this process, the number and type of tasks are also determined. A stage is executed
after its parent stages finish.

------------------------------------------------------------------------------------------------

DETAILS IN JOB SUBMISSION - (ending section on Job Physical Plans)

ResultTask or ShuffleMapTask are 2 types of tasks depending on if its after or before the shuffle
stage boundary. The tasks in a stage form a TaskSet. taskScheduler.submitTasks(taskSet) is called to
submit the whole task set.

There are extremely complicated scheduler details, refer link for details.

------------------------------------------------------------------------------------------------

SHUFFLE DETAILS -
1) In spark 1.1, default shuffle is Hash-Based
2) In spark 1.2, default will be Sort-Based and can be changed by property spark.shuffle.manager

3) Shuffle workflow in Hadoop is as follows
map() -> spill (to Local disk) -> merge -> shuffle -> sort -> reduce()
In spark, it can be split up into 2 broad categories - ShuffleWrite and ShuffleRead.

At the end of ShuffleMapStage in which there's a ShuffleMapTask.
If there is 1 worker node with 2 cores, and if there are 4 input RDD partitions, we will have 4
ShuffleMapTasks. Each core will have 2 ShuffleMapTasks (running as 2 threads).
If there are 3 output partitions => 3 reducer-side (ShuffleRead) tasks, Each ShuffleMapTask
will have to maintain R buffer files, where R = number of reducers (ShuffleReadTasks).
These buffers are called buckets and size of each bucket in Spark 1.2 is 32 KB. Its configurable by
spark.shuffle.file.buffer.kb

Contents of these buffers are spilled to disk and these on-disk files are called ShuffleBlockFile
or FileSegment. We can consolidate files of different MapShuffleTasks in each core into the same
disk file. spark.shuffle.consolidateFiles=True enables this.

SHUFFLE READ details -
1) Wait until all ShuffleMapTasks in parent stage are done and then fetch.

2) The fetched FileSegments have to be buffered in reducer-memory, so we cant fetch too much before
the buffer content is written to disk. It has default size 48 MB controlled by
spark.reducer.maxMbInFlight

3) On reducer side, if spark.shuffle.spill = False, then the write location is only memory. A
special data structure, AppendOnlyMap, is used to hold these processed data in memory. Else, the DS
used is ExternalAppendOnlyMap.

In hadoop, 70% of the memory is reserved for shuffle data. Once 66%
of this part of memory is used, Hadoop starts the merge-combine-spill process.

4) How do the tasks of the next stage know the location of the fetched data?
A) At the end of the ShuffleMapStage, the final RDD is registered with
MapOutputTrackerMaster.registerShuffle(shuffleId, rdd.partitions.size)
So reducers get the data location by querying MapOutputTrackerMaster in the driver process.
------------------------------------------------------------------------------------------------
Source - Data Engineering on Hadoop - Cloudera whitepaper
Some pitfalls to avoid in spark applications -

1)
rdd.groupByKey().mapValues(_.sum) will produce the same results
as rdd.reduceByKey(_ + _) . However, the former will transfer the entire dataset across
the network by creating a ShuffledRDD, while the latter will compute local sums for each key in
each partition (map-side combine) and combine those local sums into larger sums after shuffling.

2)
Avoid `reduceByKey` When the input and output value types are different.
rdd.map(kv => (kv._1, new Set[String]() + kv._2))
 .reduceByKey(_ ++ _)

Instead use `aggregateByKey`
val zero = new collection.mutable.Set[String]()
rdd.aggregateByKey(zero)(
 (set, v) => set += v,
 (set1, set2) => set1 ++= set2)

3)
Avoid the flatMap-join-groupBy pattern. When two datasets are already grouped by key and
you want to join them and keep them grouped, you can just use `cogroup`. That avoids all the
overhead associated with unpacking and repacking the groups.

4)
One way to avoid shuffles when joining two datasets is to take advantage of `broadcast variables`.
When one of the datasets is small enough to fit in memory in a single executor, it can be loaded
into a hash table on the driver and then broadcast to every executor. A map transformation can then
reference the hash table to do lookups.

------------------------------------------------------------------------------------------------

RDDs are stored off the JVM heap. Other off heap usages include netty’s direct buffers for shuffle and more.

Some more tips on writing efficient spark jobs with examples -
http://fdahms.com/2015/10/04/writing-efficient-spark-jobs/

Spark uses Janino compiler from org.codehaus pkg for Catalyst optimizations for DataSets. Any codehaus related exceptions
might be failures in that layer.

------------------------------------------------------------------------------------------------
NOTES FROM BIG DATA WITH SCALA & SPARK - coursera course

1) PARTITIONING -

Important: the result of partitionBy should be persisted. Otherwise, the partitioning is repeatedly applied
(involv1ing network shuffle) each time the partitioned RDD is used.

eg usage-
val pairs = purchases.map(p => (p.customerId, p.price))
val tunedPartitioner = new RangePartitioner(8, pairs)
val partitioned = pairs.partitionBy(tunedPartitioner)

2) When calling sortByKey(..) on a pairRDD, the default partitioner used is RangePartitioner.
   When calling groupByKey(..) on a pairRDD, the default partitioner used is HashPartitioner.

3) Operations on RDDs that hold and propagate a partitioner below. All other transformations and/or actions will produce
a result without a partitioner.

cogroup, groupWith, join, leftOuterJoin, rightOuterJoin, groupByKey, reduceByKey, foldByKey, combineByKey, partitionBy,
sort, mapValues (if parent has partitioner), flatMapValues (if parent has partitioner), filter(if parent has partitioner)

Note that prominently `map` operation is missing in list above because it can change the key. Hence the partitioning
strategy based on previous key becomes invalid.
------------------
SHUFFLING
4) To see execution plan and know if something has a shuffle dependency, use `toDebugString`

partitioned.reduceByKey((v1, v2) => (v1 ._1 + v2._1, v1 ._2 + v2._2))
.toDebugString

Among non-obvious operations, `distinct` and `coalesce` may cause a shuffle.
------------------
WIDE (requires N/W shuffle) VS NARROW DEPENDENCIES

    a) TX w/ narrow deps - map, mapValues, flatMap, filter, mapPartitions, mapPartitionsWithIndex
    b) TX w/ wide deps - cogroup, groupWith, join, leftOuterJoin, rightOuterJoin, groupByKey, reduceByKey, combineByKey,
        distinct, intersection, repartition, coalesce

    To find out what kind of dependence, use the `dependencies` method on RDDs. This is used internally by Spark
    scheduler.
    Narrow dep objects - OneToOneDependency, PruneDependency, RangeDependency
    Wide dependency objects - ShuffleDependency
------------------
SparkSQL uses -
    1) Catalyst - query optimizer -

    2) Tungsten - off-heap serializer.
    Spark SQL Functions use Tungsten - off-heap => There is no GC pressure. Memory
    efficient data structures. Supports rule-based optimizations. Performance is comparable
    to hand-tuned low-level operations. Aggregation, collection, math and string operations.

SprakSQL data frames are "untyped", ie uses `Rows` data type. So the scala compiler doesnt do any compile-time
type-checking about column types within a row.

import org.apache.spark.sql.SparkSession

val spark = SparkSession.builder().appName("My App").getOrCreate()

//to create a DataFrame by reading in a data source from file, use the `read`method
val df = spark.read.json("/path/to/file.json")

//register the DataFrame as a SQL temporary view
peopleDF.createOrRelaceTempView("people")
//this gives a name to a DataFrame that can be used in SQL `from` statement

------------------
DATAFRAME API -

1) `show()`  pretty prints a data frame in tabular view
    case class Employee(id: Int, fname: String, lname: String, age: Int, city: String)
    val employeeDF = sc.parallelize( ... ).toDF
    employeeDF.show()

2) employeeDF.printSchema()
    prints in nested tree format

3) Syntax for df operations - 3 types of syntax
    a) df.filter($"age" > 18)
    b) df.filter(df("age") > 18)
    c) df.filter("age > 18")

4) val sydneyEmployeesDF = employeeDF.select("id", "lname")
                                     .where("city == 'Sydney'")
                                     .orderBy("id")

5) To see methods to call after groupBY, see API of `RelationalGroupedDataset`

6) To see methods within agg, see API of spark.sql.function

7) drop() - drops rows that contain null or NaN in *any* column and returns a new DataFrame
    drop("all") drops rows that contain null or NaN values in all columns and returns a new DataFrame
    drop(Array("id", "name")) drops rows that contain null or NaN values in the specified columns and returns a new DF

8) fill(0)
    fill(Map("minBalance" -> 0))

9) replace(Array("id"), Map(1234 -> 8923)) replaces specified value (1234) in specified column (id) with specified
replacement value (8923) and returns a new DataFrame.

Common ACTIONS on DFs -
    collect(): Array[Row]
    count(): Long
    first(): Row
    head(): Row
    show(): Unit // 1st 20 rows in tabular form
    take(n: Int): Array[Row]

10) df1.join(df2, $"df1.id" === $"df2.id", "right_outer")

11)
    averagePrices.head.schema.printTreeString()    //zip: integer, avg(price): double
    val averagePricesAgain = averagePrices.map {
        row = > (row(0).aslnstance0f[Int], row(1).aslnstance0f[Double])
    }

----------------
Trade-offs of DataFrames -

Cons:
    1) Bad queries on columns that dont exist are not caught at compile time unlike scala, but at runtime. This can be
    expensive.
    2) If the data isn't structured or cannot be represented as scala case classes or std sparkSQL data types, it cannot
    be cast as DFs. Even if it is, it cannot make use of tungsten encoder's optimization for the std SparkSQL data types

Pros:
    1) Perf is 4X faster than similar operations on RDDs due to catalyst query optimizer and tungsten serialized
    encoder.
-------------------
DATASET APIs -

type DataFrame = Dataset[Row]
With Dataset, you get type safety as well as columnar representation and structured optimization using catalyst and
tungsten. RDDs are a compromise between DataFrames and RDDs.

1) listingsDS.groupByKey(l => l.zip)
          .agg(avg($"price").as[Double])

2) DataFrame uses the `Column` scala class but Dataset uses `TypedColumn`. To convert between the 2,
use $"price".as[Double]

3) Calling groupBy on a Dataset returns a RelationalGroupedDataset whose aggregation operations return a DataFrame,
but calling groupByKey on a Dataset returns a KeyValueGroupedDataset whose aggr ops return a Dataset. So to stay inside
the Dataset API, use `groupByKey` instead of `groupBy`.

4) val keyValues = List ( (3, "Me"), (1, "Thi"), (2, "Se"), (3, "ssa"), (1, "sisA"), (3, "ge : "), (3, "-) "),
        (2, "ere"), (2, "t"))

   val keyValuesDS = keyValues.toDS

    keyValuesDS.groupByKey(p => p._1)
               .mapGroups((k, vs) => (k, vs.foldLeft("")((acc, p) => ace + p._2))).show()
               .sort($"_1").show()
-------------------
5) Using an aggregator
val keyValues = List((3, "Me"), (1, "Thi"), (2, "Se"), (3, "ssa"), (1, "sisA"), (3, "ge:"), (3, "-)"), (2, "ere"),
    (2, "t"))
val keyValuesDS = keyValues.toDS
val strConcat = new Aggregator[(Int, String), String, String] {
    def zero: String = " "
    def reduce(b : String, a : (Int, String)) : String = b + a._2
    def merge(bl : String, b2 : String) : String = bl + b2
    def finish(r : String) : String = r

    override def bufferEncoder: Encoder[String] = Encoders.STRING
    override def outputEncoder: Encoder[String] = Encoders.STRING
}.toColumn

keyValuesDS.groupByKey(pair => pair._1)
           .agg(strConcat.as[String])

Encoder is tungsten internal serialization format and is 10X faster than Kryo and more memory-optimized than it as well.

2 ways to introduce encoders -
import scala.implicit._

or import org.apache.spark.sql.Encoders
---------------------------------------------------------------------
WHEN TO USE DATASETS VS DATAFRAMES VS RDDs

Use Datasets (encoders are required) when
    a) you have structured/semi-structured data
    b) You need type safety
    c) you need to work with functional APIs
    d) you need good performance but it doesnt have to be the best

Use DataFrames when
    a) You want the best possible performance automatically optimized for you
    b) You have structured/semi-structured data

Use RDDs when
    a) You have unstructured data
    b) You need to fine-tune and manage low-level details of RDD computations
    c) you have complex data types that cannot be serialized with encoders

Catalyst cannot optimize functional `filter` functions but can optimize structured `filter` (DataFrame WHERE clause)
functions. Irrespective of that, TUNGSTEN is always running under the hood of Datasets, storing and organizing data in
a highly optimized way, hence giving speed-ups over regular RDD operations.

LIMITATION: if you have data that cannot be expressed as simple scala `case` classes or SparkSQL data types, its
difficult to ensure that a Tungsten encoder exists for your data type. Eg - you have an application that uses some
complicated regular scala Class.
"""








