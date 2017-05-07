"""
https://cwiki.apache.org/confluence/display/Hive/Hive+on+Spark
Hive-on-spark design document
Map-reduce's in-built shuffle capability has the following equivalent transformations in spark -
a) partitionBy - does pure shuffling (no grouping or sorting)
b) groupByKey
c) sortByKey

Cost-based optimizer in Hive -
https://cwiki.apache.org/confluence/display/Hive/Cost-based+optimization+in+Hive

https://hortonworks.com/blog/hive-0-14-cost-based-optimizer-cbo-technical-overview/
With diagrams

https://cwiki.apache.org/confluence/display/Hive/Hive+on+Spark%3A+Join+Design+Master
Hive on Spark: Join Design Master

Tuning Hive on Spark
https://www.cloudera.com/documentation/enterprise/5-9-x/topics/admin_hos_tuning.html
"""