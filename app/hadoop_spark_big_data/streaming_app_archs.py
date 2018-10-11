"""
Global Software Architecture Conference - Software Architectures for Streaming Applications
Dr Vladimir Bacvanski - founder of SciSpike

High ingestion DB  for sensor IoT data from cars are NoSQL typically Apache Cassandra, HBase,
OpenTSDB. THen onto Kafka. High speed writes.

From collector tier, pushed into NoSQL, and batch systems like hadoop and spark.
3rd sink from collector is Real-time streaming.
---------------------
Reactive streams -
1) Consumer tells producer get(3) elements - Back pressure enables us to have resilient applications
that don't crash and die due to out-of-memory exceptions.
------------
Akka streams handles back pressure very well.

input -> function1() -> broadcast -> f2() , f4() -> merge() -> f3() -> output

Akka pros:
1) Akka DSL provides hi-level concurrency primitives.
2) Spark, flink, kafka are implemented in Akka.
3) Light-weight and lean.
4) Akka's actor model is used for ETL at Salesforce MetaMind. Good for infrequent activity like polling for status of
    spark job on EMR.
5) Akka-http has intuitive DSL with all HTTP verbs. Can do request proxying, routing, web sockets. Routes are easy to
    maintain and troubleshoot.

Akka cons:
1) Akka doesn't handle clustering (parallel data distribution) out of the box.
2) Akka was used in spark until spark 1.4 after which they migrated to their in-house built RPC.
3) Akka needs an ActorSystem. Akka-http not best for simple clients.
4) Actor model has a learning curve.
5) Akka-http comes barebones by design. CORS, CSRF need implementation (or 3rd party libraries). Other useful libraries-
    a) Circle (JSON serialization), github.com/travisbrown/circe
    b) Typesafe Config (env & cfg), github.com/typesafehub/config
    c) Slick (Scala style DSL for db queries, ORM), github.com/slick/slick
    d) HikariCP (Connection pooling), github.com/brettwooldridge/HikariCP
    e) Flyway (DB migration), flywaydb.org/
    f) akka-http-session (Authentication, JWT), github.com/softwaremill/akka-http-session
    g) akka-http-testkit (Testing), doc.akka.io

Book recommendation TODO: read Akka in Action
------------
Akka streams by company called TypeSafe : SFDC lambda hangout -

reactive mongo - async driver for Mongo.
Reactive streams is a std for async stream processing with non-blocking back pressure.

Akka streams has DSL layers on top of this.
Source[T, M] produces a stream of Ts and completes with an M.
Sink [I, M] consumes a stream of Is and completes with an M
Source ~> Sink = Graph
Materializer is what runs a Graph.

GearPump is created at Intel. Its a cluster-aware materializer. Materializer creates actors and sends msgs back n forth
under the hood.

Flow is a Reusable Stream Functor

-------------
Apache storm - Has spouts and bolts;
Bolts are the units doing computational work.

Really low latency ~ms. But simple capabilities. But its distributed.

Fault tolerance semantics is atleast-once.

Heron is another storm-like tool by Twitter which does similar things.
-------------
Next-gen systems for streaming are implementing lambda architectures.
Kappa architecture comes after lambda. It says the business logic can use the same code and doesn't
have to be re-written in multiple technologies like hadoop, storm, spark, etc.

Thus enters spark streaming.
Micro-batches give high throughput since its like batch mode.
But latency takes a hit in case of failure, since you have to replay the entire previous
micro-batch. Individual unit of micro-batches is DStream (discretized stream).

-------------
Apache Flink is natively streaming architecture. It has a variety of data sources.
They have adapters for HDFS, NoSQL DBs, RDBMs connectors etc.

Their distributed streaming runtime (DSR) runs on top of (HDFS< RDBMs, NoSQL).
Only 2 lines of code differ between streaming and batch, with all other business logic being the
same. Alibaba is the most notable adopter of Flink.

Spark structured streaming lets you query the stream with SQL.
-------------
Apache Beam is the common API.
Beam has comprehensive API for all batch and streaming applications.
Under-the-hood, beam can have different runners - spark, flink, apex, google data flow.

Google data flow is batch and stream processing engine used internally for many years now.

Devs program to the beam API, without worrying about runners under the hood.
****************************************************************************************************
----------------------------------------------------------------------------------------
SFDC Tech Talk Oct 6, 2018 : Karthik Ramaswamy
APACHE PULSAR - Broker (serving) and bookie (storage) decoupled to be scaled independently.

Broker has no state.

Bookie fsync's to Journal WAL. Once broker gets ack from all bookies, it acks back to producer. This ensures data is replicated and persisted durably. Using group commits, batch update thruput and latency improve.
--------------
ISOLATION -

Metadata needs zookeeper. For sequencing the segment. As long as any 3 bookies are available, they can keep going. Write availability is very high.

Bookie and broker failure.
------
Fencing protocol for resiliency.
2 aspects of failure - window of maintenance time, actual failure scenario.

Can cfg dont do replication until some time has elapsed.
------
In kafka, partitions are assigned to brokers permanently. A single partition entirely
stored on single node. Rentention is infinite. Capacity expansion doesnt require
expensive rebalancing of 4-5 hours of downtime.
----------------------------------------------------------------------------------------

UNIFIED MESSAGING MODEL -
jms & rabbitMQ = queueing model.

Exclusive partition.
Geo replication is 1st class citizen built into pulsar. Asynchronus replication be default.
Can be done synchronously using special type of zookeeper.
-------------
Multi-tenancy.

7-8X faster than kafka. Always journal enabled.
2.3M topics in production currently supported.
------------
Processing data modeled as streams: Access patterns -
1) pub/sub data consumed as its produced
2) heavy weight DAG compute - Done with Heron. Storm v2. Spouts/bolts. No restriction on # of stages. Spouts/bolts run in their own processes instead of threads. Helps in profiling and debuggability.
------
3) light-weight compute. TX and react to data as it arrives.
More like a lambda function.
--------
4) Interactive query of stored streams
-------
Operational issues - slow hosts, N/W issues, data skew, load variations, SLA violations
Developer issues - tracability.

2017 PAPER - SELF-REGULATING TUNING SYSTEMS
Self-tuning based on traffic, self-stabilizing, self-healing in presence of slow hosts.
------------
Q&A:
Functions are attached to tenant or namespace to know ownership of teams. Can pass CPU, memory
that the function needs. You can specify I/P and O/P topics.

Q: Schema registry. Support avro , protobuf, json, crypt.
Enforces schema registry. Notion of schema versioning.
-----
Q: Exactly-once semantics. We use dedupe mechanism using msgId and seqId. If it hasnt been ackd and failed, if the same msg comes again, they dedupe it.

Storm doesnt support notion of state. Heron supports state as higher synchrounous snapshots.
Every operator checkpoints itself and then global checkpoint is returned.

Data has to be retained b/w snapshots.
------------
Topics are grouped into bundles. Multiple bundles owned by 1 broker. If a broker is getting hot,
bundles are split and some topics are offloaded to least loaded brokers. 

"""