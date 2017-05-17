"""
Source - Data Engineering on Hadoop - Cloudera whitepaper
Some pitfalls to avoid in spark applications -

1)
rdd.groupByKey().mapValues(_.sum) will produce the same results
as rdd.reduceByKey(_ + _) . However, the former will transfer the entire dataset across
the network, while the latter will compute local sums for each key in each partition and combine
those local sums into larger sums after shuffling.

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
"""