"""
High Availability
Consistency
Partition tolerance


Amazon DynamoDB - mother of all distributed K-V stores. Most cited seminal work. TODO: read paper
LinkedIn developed Voldemort on Caltrain based on DynamoDB.

Functional requirements -
Scale out reads and writes
Low latency and high throughput

Workload - Single shot, single table operations
Single key-value gets

Data format -
Row-major - LinkedIn Espresso, MongoDB,
 Key + binary Large objects/JSON + schema version - structure of the row

Schema registry - serialize/deserialize based on the schema. This favors schema evolution.

and column-major -

Disk-based formats - eg - mongoDB
Redis - Cache

Cassandra has a delta log. Writes are appended to a delta log which is a row-based store.
This is merged in intervals. SSDs are append-only. They dont do well with updates.
Reads are always from columnar-store. Cassandra default is 1 Read, 1 Write, hence R + W !> N
when N = 3, hence its eventually consistent, but its fastest. Read from 1 server, write into 1
server. Netflix uses cassandra. Shopping cart items may also sometimes temporarily disappear.
But this cant be designed for brokerage account or bank accounts.

Read about consistent hashing. Allows minimal data movement when a server goes down.

This is used to go from partition_id -> server_id

Sharding - hash-based partitioning vs range-based partitioning.
Hash-based supports better load balancing.

Range-based is better for stream processing based on time ranges.
Or if nodes get added and dropped, you know what data range is getting impacted.
Range is easier to split and coalesce.

Replication -
Within a data center - quorum reads and writes.
Given the number of replicas is N, for strict consistency, R + W > N, W > N/2  where,
 R = number of replicas you need to consult to serve read requests
 W = number of replicas you need to consult to server write requests

Cross-data center replication.

TODO - read google's spanner paper, that maintains strict consistency across data centers.

Master-master replication
Transaction based guarantees - 2-phase commits
State machine based consensus - Paxos/RAFT - TODO - read

Cross data-center replication has to be asynchronus.
Google maintains atomic clocks - global clock in sync across all data centers.
This treats all global data centers as if they are in the same time zone.
Very high latency, 100 ms from east coast to west coast. There's something called sticky-routing
given by application layer. Last writer wins in-case of conflicts while merging values.

TODO - Read LWW conflict resolution on the same key-value from different data centers.
"""