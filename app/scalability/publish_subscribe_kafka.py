"""
Functional requirements -

1) Support multiple producers (publish) and consumers (subscribe), each consumer at
its own rate.

2) Durability guarantees - once an event is published, it is made durable. It will not
lose that event.

3) Ordering of message delivery - strict ordering, partial ordering, or no ordering
Kafka guarantees within a partition, but not a topic sharded across partitions.

At linkedIn, for internal replication espresso database, kafka is used. Mysql bin log
is parsed to get the strict ordering. A single thread is used to read the bin-log.

4) Freedom to adjust consumer offset

5) Kafka guarantees atleast-once semantics. An event that is published is guaranteed
to be seen by a subscriber, but the subscriber can see it more than once.
Even if kafka goes down, as long as storage is not fried, event 1 is persisted.
Kafka guarantees that event 1 is sent to consumer atleast-once.

Kafka does not guarantee that offsets are persisted.
----------------------------------------------------------------
Data Model - Events
    Topic: event_id, event_payload, shard_id within topic, kafka_offset within shard

Kafka allows creation of topics, each topic can have 1 or more partitions.
Each partition is a single producer-consumer queue.

Typically for guaranteed ordering, a topic has to be a single partition.

Some journalling has been done for taht event.
Server hosting that particular queue.

Each producer consumer Q is actually a log that is persisted no disk, in batches.
Checkpoints frequently.

For each subscriber, it maintains a checkpoint of subscriber offset.
If the kafka server restarts, it will start from the check-pointed offset.
Onus is on the subscriber client to ensure exactly-once semantics.


LinkedIn asks question about cluster manager design, or distributed stats aggregator.
WR/RD QPS for heart-beats is very high. Heart-beat is the data model.
Last update point of that heart beat say, 30s ago => service will notify and pull
storage node down. You cannot have a zookeeper for a zookeeper.
So for that, there are things ike gossip (or gass-up?) protocol.
"""