"""
Getting this error msg when kafka broker connects to zookeeper.

[2017-10-24 12:45:10,355] INFO I wrote this conflicted ephemeral node [{"version":1,"brokerid":0,"timestamp":"1508873998124"}] at /controller a while back in a different session, hence I will backoff for this node to be deleted by Zookeeper and retry (kafka.utils.ZkUtils$)

https://issues.apache.org/jira/browse/KAFKA-1387
Design of not deleting ephemeral node immediately on session expiration still exists on ZK 3.4.x

Kafka getting stuck creating ephemeral node it has already created when two zookeeper sessions are established in a
 very short period of time
"""