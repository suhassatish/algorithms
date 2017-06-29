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

"""