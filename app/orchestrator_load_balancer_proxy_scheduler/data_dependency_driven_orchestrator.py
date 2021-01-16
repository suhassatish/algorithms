"""
https://medium.com/swlh/data-dependency-driven-orchestration-d1bd8e1d695f
Jan 10, 2021
data dependency orchestration design patterns from LinkedIn, using Airflow

1) A DATA DEPENDENCY SERVICE can provide much better efficiency and scalability than the implementation as a trigger job
 or a client-side poke/pull task. The centralized shareable dependency metadata can serve multiple use cases beyond
 triggering dependent flows. Let’s look at some patterns:

2) The Global State Store is mutable with predefined data quality and backfill transition rules in place. We need keep
it as serverless as AWS Step Functions with rich & practical data semantics that work more efficiently for ever-expanding
 data lake. State store can store info such as data statistics at the source (kafka) and compare if the data is 99.995%
 complete and trigger events if so. ie if 99.995% of data generated in the last 5 mins to kafka has been consumed
 and generated an output in data lake.

3) Having midnight scheduled batch jobs for each data-residency time zone is more efficient than PST-midnight for all
data. So a data partition will have sub-partitions of local times of data residency with completeness info.


"""