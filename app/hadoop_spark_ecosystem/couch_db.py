"""
Fast Diskless NoSQL Databases - CouchDB

SQL for JSON called N1QL.

CouchDB is a KV store thats Consistent and Partition tolerant, but is not highly available.
ie its like Hbase as it provides strong consistency guarantees.

Eventually consistent upon disk write failures. (for hard failures, it becomes eventually consistent
). But for soft failures, it guarantees strong consistency.

When master for a partition goes down, until the replica becomes elected as a new master,
availability is sacrificed.

Use uniform hashing for partitioning.

-------
A single partition fully resides on a single node.
Clients are agnostic to partitions.
Intra-cluster replication.
Replicas of a partition on other nodes.
Master-slave model.
Replicas consume more memory. This is different from disk-based DBs. In disk-based DBs, only active
partition is kept in-mem.
-------

"""