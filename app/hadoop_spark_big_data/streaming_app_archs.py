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

Book recommendation: Akka in Action
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

-----------
"""