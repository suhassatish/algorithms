"""
https://www.youtube.com/watch?v=NVrnW3uFWQQ&feature=youtu.be
Building Highly Efficient Data Lakes using Apache Hudi - SF Big Analytics Meetup, presented by Uber speakers (June 2019)

Requirements for Data Lakes in Modern Enterprises -
*************************************************

1) Incremental DB ingestion
    a) Hi-value data - user info in RDBMS - trip, TX logs in NoSQL
    b) Replicate CRUD operations - strict ordering guarantees, zero data loss
    c) Bulk loads dont scale - adds more load to DB, wasteful re-writing of data

2) De-duping log events
    a) High-scale time series data - several Billions/day, few millions/sec. Heavily aggregated
    b) Cause of duplicates - client retries/failures/network errors; Atleast-once data pipes
    c) Over counting problems - low fidelity data, more impressions => more $

3) Transactional writes
    a) Atomic publish of data - ingestion can fail mid-way, rollback bad data
    b) Consistency guarantees - no partial data exposed, repeatable queries
    c) Snapshot isolation - time-travel queries, concurrent writers / readers

4) Unique key constraints
    a) Data Model Parity - enforce upstream primary keys, 1:1 mapping w/ src tables, great data quality!
    b) Transaction processing - eg - settling orders, fraud detection. Lakes are well suited for large scale processes

5) Faster derived data
    a) Multi-stage ETL DAGs. Very common in batch analytics, large amt of data

6) File management -
    a) small files => stress file system metadata, slow queries
    b) large files => large delays
    c) file stitching => band aid for bullet wound

7) Scalable DFS / Storage RPCs
    a) Ingestion / Query all list DFS - list folders, files, take action
    b) Single threaded vs parallel
    c) Subtle gotchas / differences -
        i)   Cloud storage => no append()
        ii)  S3 => eventual consistency, rename() == copy()
        iii) Large directory listings

8) Incremental copy to data marts
    a) OLAP DWH ingesting from data lake
    b) Online serving - sync ML features to DBs, throttling syncing rate.

9) Legal requirements / data deletions
    a) Strict rules on data retention - delete records, correct data, raw + derived tables
    b) Need efficient delete() - indexed on write but optimized for scans. Propagate deleted records downstream.

10) Late data handling
    a) Mins, hrs even days - eg - credit card Txn settlement
    b) Not implicitly complete - can lead to large data quality issues; trigger recomputation of derived tables.
    c) Data arrival tracking - 1st class audit log, flexible, rewindable windowing.
--------

Future - Support watermarks like apache beam for composing safe, incremental pipelines. This can hide flink or spark
implementations under the hood.

"""