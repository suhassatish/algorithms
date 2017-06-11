"""
Use cases for Redis applications - Deployed in-front of DB for low-latency caching.

Redis architecture-
1) Single-threaded, in-mem engine with persistence.

2) Lock-free arch for fast execution.

3) Optimized for hi-speed access

4) Persistence with AOF (?) or snapshot disk durability.

5) Shared-nothing cluster architecture.

6) auto fail-over, auto-scaling without downtime.

7) 99.9999s of availability

8) Keeps in-memory hash-map of key-value pairs.

9) Written in C

10) Extensible through redis modules - tensorFlow module instantiates tensors in the DB;
another module takes RandomForest, regression etc from Spark and run them in redis - called redisML
module, neural network trained inside redis in ms and serves recommendations directly out of redis.

11) 2 MB foot print. So good in embedded flight control systems with limited memory.

Some other modules - over 50 available now. Like search indexing, time series processing, etc.

Sub-ms latency = typical for redis. Very difficult to use spark to serve recommendations out of
spark with millisecond latencies. RedisML is 13X faster than SparkML.
Try it databricks notebook -
https://bit.ly/sparkredisml

--------------------
Can have part of data in tables, parts in json, etc. Hetergenous types of backend data can be
cached by 1 redis caching layer.
--------------------
ML model serving challenges -
1) Bigger sizes as models become more precise and complex.

2) Recos in mission-critical apps - scaling, perf, HA, DR

3) managing multiple model types - logistic regr, GB trees, RF

4) Multiple versions of models

5) distributed model upgrade.

6) Training and serving apps maybe written in different languages.

"""