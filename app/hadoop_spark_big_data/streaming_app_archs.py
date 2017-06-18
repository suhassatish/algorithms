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
Akka DSL provides hi-level concurrency primitives.
Spark, flink, kafka are implemented in Akka.
Light-weight and lean.

Akka cons:
Akka doesn't handle clustering (parallel data distribution) out of the box.

Book recommendation: Akka in Action
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