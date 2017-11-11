#!/usr/bin/env bash

#kafka project is packaged with a zookeeper for running locally.
#Download the pre-compiled binary for version kafka_2.10-0.8.1.1

#1)
bin/zookeeper-server-start.sh config/zookeeper.properties
#Listens on port 2181 by default

#2) # start a kafka broker (each broker should have a unique ID)
bin/kafka-server-start.sh config/server.properties
#INFO conflict in /controller data: {"version":1,"brokerid":1,"timestamp":"1508875153082"}
#stored data: {"version":1,"brokerid":0,"timestamp":"1508873998105"} (kafka.utils.ZkUtils$)

# Listens on port 9092 by default
# Registered broker 1 at path /brokers/ids/1 with address ssatish-ltm.internal.salesforce.com:9092

#3) create a topic
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic beacon.pixel_gif

#4) list the topics
bin/kafka-topics.sh --list --zookeeper localhost:2181

#5) Run a producer and type a few messages or use fluentd to stream msgs to a topic
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test2

#6) to consume msgs -
bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test2 --from-beginning

#7) Kafka broker logs are under tmp/kafka-logs, also configurable in server.properties

#---------------------------------------------------------------------------------------

#You need to adjust three (or four) properties:
#
#Consumer side:fetch.message.max.bytes - this will determine the largest size of a message that can be fetched by the consumer.

#Broker side: replica.fetch.max.bytes - this will allow for the replicas in the brokers to send messages within the cluster and make sure the messages are replicated correctly. If this is too small, then the message will never be replicated, and therefore, the consumer will never see the message because the message will never be committed (fully replicated).

#Broker side: message.max.bytes - this is the largest size of the message that can be received by the broker from a producer.

#Broker side (per topic): max.message.bytes - this is the largest size of the message the broker will allow to be appended to the topic. This size is validated pre-compression. (Defaults to broker's message.max.bytes.)
#---------------------------------------------------------------------------------------

# kafka producer with a cat
cat ~/features/attribute_metrics/beacons/beacon-a271.krxd.net+pixel.gif-2017-10-24-18-00.log | bin/kafka-console-producer.sh --broker-list localhost:9092 --topic beacon.pixel_gif
#---------------------------------------------------------------------------------------
# to see how much is a kafka consumer-group topic lag - (not supported in kafka 1.0)
 /usr/local/kafka/bin/kafka-run-class.sh kafka.tools.ConsumerOffsetChecker --broker-info  --group com_krux_spark_streaming_jobs_PixelStreamProcessor --topic beacon.pixel_gif --zkconnect zookeeper-a003.krxd.net:2181/kafka-beacon-a