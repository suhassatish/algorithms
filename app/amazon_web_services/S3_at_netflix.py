"""
AWS re:Invent 2016 - Netflix: Using Amazon S3 as the fabric of our big data ecosystem (BDM306)
https://www.youtube.com/watch?v=o52vMQ4Ey9I

At Netflix, amazon S3 (Simple Storage Service) is the centralized data hub.

Pros of S3 -
1) Cloud native service (free engineering).
2) Decouples compute and storage.
3) Practically infinitely scalable
4) 99.99% available
5) 99.999999999% durable

Cons of S3 -
1) Eventually consistent
2) Performance is slow - since cloud based service is remote from your cluster

Data volume on S3 -
1.5 Billion objects
Data hub 60 PB data (Dec 2016) => Read about 3.5 PB daily for ETL processing; WR 500+ TB/day
Expiration - 400+ TB daily
Data velocity: 100+ TB data/day
------------------------------------------------------------------------
2 data pipelines at Netflix - Event & Dimension data pipeline.

Event data pipeline for business events -
1) ~500 Billion events/day
2) 5 min SLA from source to data hub

Netflix hosted in 3 different AWS regions. Each region has its own kafka pipeline.
Region1: Cloud_apps => Kafka => AWS S3
                          \-> SQS (Simple queuing service)


Region1 S3/SQS -> -|
                   V
Region2 S3/SQS -> Ursula -> Data Hub
                   ^
Region3 S3/SQS -> -|
Ursula reads about 6M files/day across all regions. Ursula groups and merges kafka topics from
event streams and publishes to data hub.
-----
Dimension data pipeline - This is for stateful data in Cassandra clusters

Extracts from tens of Cassandra clusters
Daily or more granular data extracts.

Region1 => Cassandra Cluster backed by SS tables on AWS S3->|
                                                            V
Region2 => Cassandra Cluster backed by SS tables on AWS S3  => Aegisthus => Data Hub
                                                            ^
Region3 => Cassandra Cluster backed by SS tables on AWS S3->|

Cassandra cluster replicated across 3 different regions.
Cassandra clusters updated incrementally.

Aegisthus is a bulk data extraction pipeline.
------------------------------------------------------------------------
Hive, Pig, Spark run on top of Hadoop Yarn clusters running on Amazon EMR.
Spark was introduced at the beginning of 2016 in Netflix big data platform
and will soon replace pig use cases. Spark MLLIB also has potential.

Presto for interactive adhoc queries (with support for windowed aggregations) is running on EC2,
and is replacing hive use cases quickly.

Hadoop YARN cluster size - 3,500 d2.4XL
presto cluster size - 250-400 r3.4XL

1 d2.4XL has 24 TB storage space. So to store 60 PB data, you will need 60,000 TB/24 TB = 2.5K
machines. To achieve 3-way replication in each region, will need 3 times the number of machines
= 7.5k d2.4XLs. So the data size is beyond what can be fit into the clusters.

Hence the need to scale compute and storage separately.
------------------------------------------------------------------------
Trade-offs of eventual consistency -
1) Put operation in S3 is eventually consistent. Netflix side-steps it by creating a new file name
and deleting the old one during updates. ie, Put new files with new keys (file-names) when updating
data, then delete old files.

"""