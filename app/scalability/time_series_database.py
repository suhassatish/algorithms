"""
Query patterns: How many times in last 5 minutes, etc

Any DB can be used if schema is well thought out.

1) List of possible requirements of a TSDB -
https://softwareengineering.stackexchange.com/questions/269590/how-to-efficiently-store-big-time-series-data
https://www.xaprb.com/blog/2014/06/08/time-series-database-requirements/

2) Optimizing a relational DB for TS data
Short, 5-minute video, but lays the foundation well.
https://www.youtube.com/watch?v=X4TfveHzBwM

3) Using a columnar DB as TSDB. A little cursory but sets the foundation well
https://medium.com/@hellomichibye/column-oriented-database-draft-part-2-21199a2de18a

4) Cassandra for TSDB -
https://academy.datastax.com/resources/getting-started-time-series-data-modeling
https://www.datastax.com/dev/blog/advanced-time-series-with-cassandra

5) Mongo schema for TSDB
https://www.mongodb.com/blog/post/schema-design-for-time-series-data-in-mongodb

6) http://jmoiron.net/blog/thoughts-on-timeseries-databases

"""