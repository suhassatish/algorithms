"""
http://blog.cloudera.com/blog/2014/05/apache-spark-resource-management-and-yarn-app-models/

Spark can be launched in local-mode or in cluster-mode.
Cluster-mode has a cluster manager which can be either yarn, or mesos, or spark-standalone in-built
cluster manager.

In cluster mode with yarn, there are 2 sub-modes
1) yarn-client mode
2) yarn-cluster mode

The following chart lists the differences between these modes
                              | Yarn cluster     | Yarn Client|Spark Standalone      |
------------------------------|------------------|------------|----------------------|
Driver runs in                |application master|Client      |Client                |
Who requests resources?       |application master|AM          |Client                |
Who starts executor processes?|YARN NodeManager  |YARN NM     |Spark Slave           |
Persistent services           |YARN RM and NM    |YARN RM & NM|Spark Master & workers|
Supports spark shell?         |No                |Yes         |Yes                   |

In yarn-mode, each application can configure the number of executors to launch, but in spark
standalone mode, each application launches 1 executor JVM on each worker node.
All executors are of the same JVM size (as of mid-2014), but YARN is working on dynamic resizing
of yarn containers and hence the JVM processes.

Within the executors, tasks run either serially or concurrently as threads. The executor JVM
is re-used and persists for the lifetime of the application, even after the task is finished running
This helps in atleast 2 ways to speed-up execution in spark compared to map-reduce -
1) caching data in-memory of the executor JVM,
2) less overhead in only 1-time start-up time to spawn JVMs per application.

------------------------------------------------------------------------------------------------

YARN FAIR SCHEDULER -
http://hadoop.apache.org/docs/r2.4.1/hadoop-yarn/hadoop-yarn-site/FairScheduler.html

1) Fairness based only on memory by default.
But it can be configured to schedule with both CPU and memory, using the notion of Dominant
Resource Fairness.

2) When there is a single app running, it uses the entire cluster. When other apps are launched,
resources that free up are assigned. Eventually, each app gets the same amount of resources.

3) Unlike the Hadoop scheduler which queues all apps, the fair scheduler lets short apps finish
quickly without starving long-running apps.

4) Fair sharing can also work with app priorities which are used as weights to determine fraction
of total resources that each app should get.

5) Scheduler organizes apps into queues and shares resources fairly between these queue. By default,
all users share a single queue, named 'default', unless explicitly requested for a specific queue.

6) "Guaranteed minimum shares" per queue can be configured

7) A running application can be moved to a different queue.

8) Supports heirarchical queues with pluggable policies

9) A policy consistes of a set of rules to classify an application into a specific queue. Each rule
either adds an app onto a queue, rejects it or continues onto the next rule.

10) MODIFYING CFG AT RUNTIME - properties in separate file mentioned in yarn-site.xml are polled
and any change is picked up within a few seconds to change the queue configurations
"""