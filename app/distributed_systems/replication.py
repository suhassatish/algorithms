"""
Martin Kleppman - Big Ideas Behind Reliable, Scalable and Maintainable Systems
Chapter 5 - Replication

LEADERS AND FOLLOWERS - aka master/slave or active/passive model
    a) 1 of the replicas is designated the leader aka primary for writes. It 1st WR to its local
    storage.

    b) In postgreSQL, `hot standby` refers to a replica that accepts reads from clients. A `warm
    standby` processes changes from the leader, but doesn't process any queries from clients. As
    part of replication log or change stream, when leader writes new data, it sends the data change
    to all its followers. All writes are applied in the same order as they were on the leader.

    c) Readers can read from leader or replicas (maybe stale).
------------------------------------------------------------------------------------------------
SYNCHRONOUS VS ASYNCHRONOUS REPLICATION - In relational DBs, this is configurable, but hard-coded
in other systems.

    a) Synchronous replication is when leader waits until replica is updated before acknowledging to
    user (client).

    b) Good trade-off is to have 2 replicas - 1 synchronous and 1 asynchronous. Figure 5-2, page 154
    This is also sometimes called semi-synchronous.

    c) Most of the time, followers catch up in < 1s. But sometimes, can lag behind by minutes if
    recovering from a failure.

    d) Fully asynchronous replication maintains high write throughput although followers have fallen
    behind, by sacrificing durability. A write is not guaranteed to be durable although it has
    confirmed to the client.
------------------------------------------------------------------------------------------------
SETTING UP NEW FOLLOWERS -

    a) Take a snapshot dump of DB at a given time. That point in time in postgreSQL is called log
    sequence number. In mySQL, its called binlog co-ordinates.

    b) Follower starts from the snapshot and copies all new events from change data capture since
    the snapshot timestamp.

    c) In github, when mysql primary failed-over and lagging follower got leader elected, its
    auto-incrementing primary id was behind, but redis cache was updated. This led to different
    users being shown private data of different users.
------------------------------------------------------------------------------------------------
DIFFERENT TYPES OF REPLICATION -

1) Statement-based replication -
    a) Every INSERT, UPDATE, DELETE statement is sent to every replica, as if from client.
    Breaks down when non-deterministic cmds like NOW() and RAND() are called, which may generate
    different values on primary and replicas.

    b) Mysql before 5.1 was using this, but changed to row-based since statement-based had many edge
    cases.

    c) VoltDB uses statement-based replication, and makes it safe by requiring transactions
    to be deterministic.

    d) Statements that have side effects (e.g., triggers, stored procedures, user-defined
    functions) may result in different side effects occurring on each replica, unless
    the side effects are absolutely deterministic.

2) WAL shipping - Used in postgreSQL and oracle.
    Disadvantages:
        a) WAL contains details of which bytes were changed in which disk blocks. This makes
        replication closely coupled to the storage engine. If DB changes its storage format from
        1 version to other (eg - postgres 8.x vs 9.x), its not possible to run different versions
        of DB server of leader and follower.

        b) Due to a) cannot have zero-downtime upgrades with updating follower first and then
        failing over.

3) Logical (row-based) log replication: Different log formats for replication and storage engine to
decouple them.
    A transaction that modifies several rows generates several such log records, followed
    by a record indicating that the transaction was committed. MySQL's binlog (when
    configured to use row-based replication) uses this approach

4) Trigger-based replication: Client-application triggers the replication rather than the DB server.
    a) A trigger lets you register custom application code that is automatically executed
    when a data change (write transaction) occurs in a database system. The trigger has
    the opportunity to log this change into a separate table, from which it can be read by
    an external process. That external process can then apply any necessary application
    logic and replicate the data change to another system. Databus for Oracle and
    Bucardo for Postgres work like this, for example.

    b) Trigger-based replication typically has greater overheads than other replication
    methods, and is more prone to bugs and limitations than the database's built-in replication.
    However, it can nevertheless be useful due to its flexibility.
------------------------------------------------------------------------------------------------
PROBLEMS WITH REPLICATION LAG -

1) READ-AFTER-WRITE CONSISTENCY OR READ-YOUR-WRITES CONSISTENCY: If user writes (eg - posts a
comment) and tries to immediately read (read is served from replica while write goes to primary),
user may not see the comment since follower hasn't caught upto leader and is geo-replicated
asynchronously to serve users half-way round the world (eg - Singapore data center serving India).

    Work-arounds:
    a) When reading something the user has written, read from leader. Else, read from
    follower.

    b) The client can remember the timestamp of its most recent write. Then the system
    can ensure that the replica serving any reads for that user reflects updates at
    least until that timestamp

CROSS-DEVICE READ-AFTER-WRITE CONSISTENCY: eg - Updates from mobile need to be quickly reflected on
web app for same user.
    Consideration: if the user's desktop computer uses the home broadband connection and their
     mobile device uses the cellular data network, the devices' network routes may be completely
     different.) If your approach requires reading from the leader, you may first need to route
     requests from all of a user's devices to the same datacenter.

2) MONOTONIC READS - eg - Upon refreshing page, friend's comment has disappeared due to request
routed to lagging follower upon refresh. User sees things moving backward in time. Monotonic read
guarantee prevents this from happening. Its a lesser guarantee than strong consistency, but better
than eventual consistency.
    If one user makes several reads in sequence, they will not see time go backward
    i.e., they will not read older data after having previously read newer data.

    How to achieve it: Replica can be based on hash(user_id) so a particular user always goes to the
    same replica.

3) CONSISTENT PREFIX READ GUARANTEE: This guarantee says that if a sequence of writes happens in a
certain order, then anyone reading those writes will see them appear in the same order.

    work around to prevent inconsistency: All writes that are causally realted to each other are
    written to the same partition.
----------------------------------------------------------------------------------------------------
MULTI-LEADER/MULTI-DATA CENTER OR ACTIVE-ACTIVE/MASTER-MASTER REPLICATION

1) Supported in the following DBs - Tungsten Replicator for MySQL, BDR for PostgreSQL,
    and GoldenGate for Oracle. But, autoincrementing keys, triggers, and integrity constraints can
    be problematic. Hence, multi-leader replication is often considered dangerous territory that
    should be avoided if possible. CouchDB is designed for this mode of operation

2) Application - Calendar application on mobile phones when you make a change to meeting invite on
your phone while not connected to internet. Each device is a 'datacenter', and the network
connection between them is extremely unreliable. Write to primary (on phone) which gets async
replicated to server when there is internet.

3) Google docs shared editing is another application. For faster syncing, avoid locking and make the
unit of change very small, like a single key stroke.

4) Handling write conflicts:
    a) Conflict free replicated datatypes (CRDTs) are a family of data structures
    for sets, maps, ordered lists, counters, etc. that can be concurrently edited by
    multiple users, and which automatically resolve conflicts in sensible ways. Some
    CRDTs have been implemented in Riak 2.0.

    b) Mergeable persistent data structures track history explicitly, similarly to the
    Git version control system, and use a three-way merge function (whereas CRDTs
    use two-way merges).

    c) "Operational transformation" is the conflict resolution algorithm behind collaborative
    editing applications such as Etherpad and Google Docs. It
    was designed particularly for concurrent editing of an ordered list of items, such
    as the list of characters that constitute a text document.

    d) When there's an insert followed by an update event, to correctly order them in multi-master
    systems, a technique called "version vectors" can be used (Collection of version numbers from
    all replicas is called version vector.). Version vectors are sent from the database
    replicas to clients when values are read, and need to be sent back to the database
    when a value is subsequently written. (Riak encodes the version vector as a string that
    it calls causal context.) The version vector allows the database to distinguish between
    overwrites and concurrent writes.

    e) Conflict detection techniques are
    poorly implemented in many multi-leader replication systems. For example, at the time of writing
    this book, PostgreSQL BDR does not provide causal ordering of writes, and Tungsten Replicator
    for MySQL doesn't even try to detect conflicts

    f) Read repair: Whats the use of telling a client about staleness of a read? (Asked by Parth
    Brahmbhatt at Netflix onsite in the context of HBase) Answer: Read-repair. If read issued to
    3 nodes (1 master + 2 replicas) in parallel, and 2 of them return with version:7 and 1 of them
    with version 6, then the client sees a stale value and writes the updated version 7 into that
    node. This approach works well for values that are frequently read.
----------------------------------------------------------------------------------------------------
LEADERLESS REPLICATION
Clients send each write to several nodes, and read from several nodes in parallel
in order to detect and correct nodes with stale data.

SLOPPY QUORUM AND HINTED HANDOFF -
HINTED HANDOFF -
writes and reads still require w and r successful responses, but those may include nodes that are
not among the designated n 'home' nodes for a value. By analogy, if you lock yourself out of your
house, you may knock on the neighbor's door and ask whether you may stay on their couch temporarily.

Once the network interruption is fixed, any writes that one node temporarily
accepted on behalf of another node are sent to the appropriate 'home' nodes. This is called hinted
handoff. (Once you find the keys to your house again, your neighbor politely asks you to get off
their couch and go home.)

"Sloppy quorums" are particularly useful for increasing write availability: as long as any
w nodes are available, the database can accept writes. However, this means that even
when w + r > n, you cannot be sure to read the latest value for a key, because the
latest value may have been temporarily written to some nodes outside of n.

A sloppy quorum actually isnt a quorum at all in the traditional sense. Its only
an assurance of durability, namely that the data is stored on w nodes somewhere.
There is no guarantee that a read of r nodes will see it until the hinted handoff has
completed.

Sloppy quorums are optional in all common Dynamo implementations. In Riak they
are enabled by default, and in Cassandra and Voldemort they are disabled by default.
----------------------------------------------------------------------------------------------------

TODO - 
1) paper (blog entry)  on distr systems - Linearizability vs Serializability paper by Peter Bailis

2) Jeff Dean's paper from Feb 2013 - tail at scale by Jeff Dean and Luiz Andre Barosso - communications of ACM
---------------

COMMON APPLICATIONS AND PATTERNS
                            | Low Latency        | Low Latency        | Read Your Writes |Comment
                            | Predictable Reads? | Preditable Writes? |                  |
Careful Replacement of K/Vs |    No              |   No               |  Yes             |Work across multiple key/values   
TXI blobs-by-ref            |   Yes              |  Yes               |  Immutable       |Non-linearizable plus immutable
Ecommerce shopping cart     |   Yes              |  Yes               |   No             |Sometimes gives stale result
Ecommerce product catalog   |   Yes              |   No               |   No             |Scalable cache -> Stale OK
Search                      |   Yes              |   No               |   No             |Scalable cache plus search
Append to Big Files         |   Yes              |   No               |  Immutable       |File append semantics require linearizability of appends

Linearizability and "read your writes" are not always required in modern scalable applicatios. Thruput, not latency matters.

"""
