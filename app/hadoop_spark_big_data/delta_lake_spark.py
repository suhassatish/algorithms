"""
Delta Lake - DML internals
How do Delete, Update, Merge work
-----------------------
Delta lake keeps all the metadata in the transaction log vs in the metastore.

In spark v < 3.0, theres no API to directly read and write from external metastores.

delta lake 0.7.0 to be released with OSS spark 3.0 can work with Hive metastore.
----

Delta has command to generate these manifest files to be ingested with Presto.
Presto doesnt directly read TX log but instead reads manifest files.


"""