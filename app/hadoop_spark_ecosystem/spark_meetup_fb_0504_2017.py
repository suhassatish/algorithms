"""
Dan Weeks-

Data at Netflix -
Feedback from services, cloud constitutes majority of the data.
500 Billion to 1 Trillion peak events thru kafka/day
60 PB DWH
Read 5 PB
Write 300 TB


Big Data Platform Architecture -
Event data -> cloud services -> Kafka -> Ursula (puts into large files) -> AWS S3
                                                                            ^
Dimension data -> Cassandra -> SS Tables in S3 -> Agesthis------------------|

Service - genie, metacat metadata
Compute engines - spark, presto, druid, hive, pig
storage - S3, parquet
-------
prod - 3400 d2.4XL clusters 355 TB memory

ad-hoc
125 TB memory

Runs Spark on YARN.
1) multi-tenancy works really well in YARN
2)spark version support (Genie handles cluster cfgs, like federated execution service)
- can run multiple versions of spark at the same time. Can support ppl who need new
 features, who need stability, etc

Netflix Key Spark Metrics -
~450 users
~40% prod read volume

2k containers (6k vcore); Largest.
3 cores/container; 6k threads sometimes;

Select Topics -
1) File catalog implementation -
  a) default catalog lists all paths under a table
  b) expensive for large tables
  c) leverage hive metastore for partition pruning

2) S3 output committer -
  a) S3 doesnt have rename semantics, its a full copy - spill the data on local disk.
    does multi-part upload, but dont commit. Driver commits the job. In hive u cant
    append to a partition.

3) Parquet filter pushdown -
  a) use case - Selective access pattern to huge amt of data.
  b) consolidated logging. Even with 4-level deep partitioning in hive, u still have
   too much data. Cannot scale with partitions. Pressure on hive metastore.
   Global sort, push down into parquet which reads metadata. THen you process only
   small portion of dataset. Works with any tool that supports parquet filtering.
  c) Spark has 2 read paths - native read path and hive read path.
  In native, we have parquet filtering.

4) Dynamic allocation - Any data skew can allocate 1ks of resources. Has been in spark
since 1.2. At 1.6, can handle 500 executors, but beyond that there would be communication
problems due to timeout, N/W disruption, etc.
By 2.0, things got quite a bit better. How does spark communicate thru resource manager?


5) Range partitioning calculations -
  a) Impacts SLA for large jobs - harvest info from previous executions,
  to see whats the correct range partitioning for a job. GOal is to provide nice
  syntax to determine data skew.

  b) Wasted resources

6) Apache Toree - Notebooks/Console
    a) Spark REPL doesnt have syntax highlighting; Toree backend gives u all that
    like ipython,including multi-line cmds.
-----------------------------------
Spark on a Disaggregated Compute & Storage Architecture
Ergin Seyfe
Brian Cho

1) Disaggregated Compute & Storage Architecture
  a) Compute & storage are collocated on a spark cluster.

DFS - warm storage is a DFS based on RSA encoding
TempFS is light weight, k-V store, built on warm-storage. Used as replacement for
local disk.

Spill, cache and shuffle operations in spark go to warm-storage.

Why disaggregated?
To scale storage and compute separately.

Capacity planning can be done separately.

Performance challenges -

N/W - latency is bottleneck, not B/W
Disk - IOPS is the bottlencek. Shuffle reads dominate IOPS.
To decrease # of shuffle read reqs, took idea of aggr at end of mapper, from sailfish paper.

Disk model - read size vs read time
soln 1) Buffered spill and cache

soln 2) asynchronous shuffle (supported by tempfs)
this compresses time you need to shuffle

Current status -
100 TB i/p & 60 TB shuffles.
----------------------------------
How does spark support deep learning?
A) tensor frames - columnar format that TensorFlow understands. TensorFlow is like a UDF to Spark.
Native code execution in Spark feature - publish some hooks and data format.
Deep Learning on Apache Spark - resources?
TODO
----------------------------------
Q) Aggregate pushdown available into data source?
A) Its WIP, not in open source spark core yet.

Q) Manually repartition data frame to bring number of tasks down. Is there any plan to
intelligently do it?
A) custom coalesce function exists if you have better idea of how to combine and coalesce your data.

Q) SS tables are back-up tables for Cassandra. Custom map-reduce jobs read out of it.
A)

Q) trade off of large vs small clusters?
A) any individual cluster may not be large enough for any job.

2 large jobs should not run on the same small cluster.
Better to have a unified large cluster, and get hadoop, yarn and everything to scale.
YARN fair scheduler to divide up the work.


"""
