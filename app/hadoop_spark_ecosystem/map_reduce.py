"""
Map-side Combiner is a special type of reducer that reduces the many outputs from a mapper for the
same key before writing to disk & then shuffling it across the network.
A combiner must be commutative and associative, which means irrespective of order of combining input
it must produce the same result.

Shuffle:Groups key-value pairs with the same keys by shuffling data across the cluster's
network.

Hadoop Map-reduce also supports custom partitioning via a Partitioner (to distribute data equally
to all reducers) and custom grouping for reducer via grouping Comparator. Both map-reduce and spark
use hashPartitioning as the default partitioning strategy.

`Context` objects give access to a `Counter` API for accumulating statistics.
A reducer always sees keys in sorted order within its life time.

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

"""