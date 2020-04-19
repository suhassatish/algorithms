"""
DECOUPLING PRESTO FROM THE HIVE DATA WAREHOUSE - Alluxio Tech Talk - 2020/03/24

Alluxio talk - how presto and hive together has inefficiencies and how alluxio solves it -

Presto has an embedded hive connector which talks to hive metastore and to hive storage

Potential inefficiencies -
1) overloaded / slow hive metastore
2) un-optimized file formats (csv or parquet/ORC)
3) inefficient table data organization (too many small files)
4) inability to change or update how data is stored
------------

Benefits of Alluxio Data Orchestration -
1) Caching
2) Unified Interface/ Namespace
3) Schema-Aware Optz
4) Compute-Optimized Formats
5) Physical Data Independence
----
Storage-optimized data format -> Transformation Service -> compute-optimized data format

1) Attached existing Hive database into Alluxio Catalog
2) Alluxio Catalog served table metadata for Presto
3) Transformed store_sales by coalescing and converting CSV to Parquet

---------
1) Does CSV to Parquet TX support nested-array type?
2) Some larger clusters run into issues with HDFS namenode and switch to federated name node. How does Alluxio caching functionality work?
Its primarily caching the file data contents. It wont access HDFS when looking up from Alluxio cache.

3) How is it used in public cloud env?
    a) Alluxio has bootstrap script with EMR to be deployed together.
    b) Manually deploy to EC2 machines

4) Does alluxio served metadata serve anything in hive metastore? Can it be used without hive metastore?
    A. Catalog service reads all metadata from hive metastore to present to presto.

5) AWS glue catalog is good for EMR. Is Alluxio catalog like glue catalog? If not, are there plans to do so?
    A. Alluxio catalog can connect to an existing glue catalog.

6) Does the new catalog have repair functionality like Hive connector?
    A. DDL, DML, repair, analyze table and such commands are being added.

7) Can existing clusters have alluxio added without any disruption?
    A.

8) Large tables with many partitions. How does it work?
    A. When a DB is attached. Can filter out some namespaces. General scalability of catalog service is being looked into actively.

9) Can the new catalog service be used with spark also?
    A. Not today. But can swap with presto connectors.

10) Perf diff when cache misses in alluxio?
    A. Alluxio reads from the datastore. Avg file size for coalesce? Its configurable in Tx definition. Default = 2GB

11) Which parquet version does this support?

12) orc service to alluxio structured service?

If you use presto connector, you only interact with alluxio catalog service.

13) Additional CPU or RAM required for alluxio? It typically depends on the work load and components.
Workers need local storage. IO to transfer data in and out of the machine.
"""