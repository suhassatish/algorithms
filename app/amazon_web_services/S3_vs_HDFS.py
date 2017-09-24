"""
Amazon S3 Facts:
1) Its an object store, not a file system strictly - no concept of a folder, only a concept of a key. S3 access and
stores as key:object tuple.

2) S3 uses eventual consistency model - discp utility may face an issue saying a container was written-to on S3, but
another process cannot verify the write.
---------------
Decision parameters:
1) Agility and decoupling: S3 elastically scales the storage. Decouples compute scaling in EC2. Using HDFS doesn't give
you this flexibility.

2) Cost: S3 is 10X more cost effective than the equivalent like EBS (elastic block storage - provides HA blk-level
storage volumes for use with EC2 instances). EBS volumes are not ephemeral, ie they dont disappear when an instance
fails or is terminated. Data on EBS can be snapshot-backed up on S3 (but not in user-visible bucket).
Snapshots are incremental, ie only blocks that have
changed since previous snapshot are saved. 1 EBS volume (if you use Zadara cloud block storage) can be attached to
multiple EC2 instances, either with iSCSI and/or NFS.
S3 cost:
1st 50 TB/month: 0.039/GB  0.02/GB (infrequent access glacier storage)
Next 450 TB/mo:  0.037/GB  0.02/GB
Over 500 TB/mo   0.0355/GB 0.02/GB
S3 also supports storing compressed files. Amazon also takes care of S3 backups automatically, where as HDFS 2-3X
replication eats into the storage you pay for.

AWS Elastic Beanstalk is an orchestration service for deploying infrastructure including EC2, S3, SNS (simple
notification service), cloudWatch, autoscaling, elastic load balancers (ELB), etc

3) SLA (Durability and uptime) - S3 gives 99.99..going to 11 decimal places.

4) Performance - HDFS shines here. Data is more local. RD/WR are 2-3 times faster on HDFS, due to data locality.
Spark uses 3-4 times smaller blocks on S3 => more parallelism can be used if u have more compute cores or nodes for
spark.
       | HDFS on ephemeral storage | Amazon S3
Read:  | 350 Mbps/node             | 120 Mbps/node
Write: | 200 Mbps/node             | 100 Mbps/node


5) Design considerations - Unique characters on the key need to be on the left side, immediately after bucket name.

6) Limitations - HDFS has problem storing really small files.
It is detailed here - http://blog.cloudera.com/blog/2009/02/the-small-files-problem/
Every file, directory and block in HDFS is represented as an object in NameNode's memory occupying ~150 Bytes.
So 10M files use up about 1.5 GB memory. So 1 Billion files is not feasible. HDFS is optimized for streaming sequential
reads of large files with data locality. Reading a lot of small files requires inefficient random disk access with lot
of overhead. Also, each map-task processes a small file and lots of mappers are required.
2 ways to alleviate this - `MultiFileInputSplit` can run multiple splits per map, and mapred.job.reuse.jvm.num.tasks
can reuse JVM of a mapper to avoid start-up overhead.

They should be concatenated or unified to Hadoop Archives.
Also, data on a cluster is not accessible outside the cluster.

However, S3 files can have a max size of 5 GB. Additionally, S3 doesnt support orc and other file formats.

-----------------
Hybrid approach - Use frequently accessed, fast-processing data on hadoop HDFS medium-long term cluster.
S3 can be used to store long-term data, very large data sets and infrequently used data.

Amazon S3 distcp (map-reduce based tool) can be used to move huge volumes of data between HDFS and S3.
Data frames pointing to parquet files in S3 can be queried from hive or impala or spark
eg usage - `hadoop distcp s3://<s3_bucket>/orc/ /`
`hdfs dfs -ls /orc/`
"""