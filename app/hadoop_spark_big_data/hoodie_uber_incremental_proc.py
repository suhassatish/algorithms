"""
Meetup on Wed, July 26, 2017:
Vinodh, Tech Lead Hoodie at Uber Data, ex-LinkedIn lead on Voldemort === LIn's Cassandra

github.com/uber/hoodie
eng.uber.com/hoodie

Index: Gives info of which files contain a key
Data Files:
Timeline Metadata: Like redo or commit log.

Views: How you read data by different query processing read engines like hive, presto, spark, etc

Bloom index is built-in with hoodie.

client.upsert(inputRecords, commitTime)

commitTime is write time.
----------------------------------------------------------------------------------------
Deep Dive:

Storage types (write):
a) Copy-on-write (versions files) : Design goal: No hit on query perf. Ingest latency has to go down.
    select * from t; Read Optimized for scans;
    LogView - Gives incremental

b) Merge on read: Compactor. Like HBase.
    ReadOptimized
    LogView
    RealTime
    Avro row-based format + Parquet columnar format;
----------------------------------------------------------------------------------------
Data Skew: Straggler problem?
Spark if you shuffle > 2 GB in a partition, it slows down tremedously.
Hoodie uses statistics in the input data to make sure DAG is balanced.




"""