"""
/*
There are two datasets, stored in HDFS:
Dataset 1: User interactions. Stored in hdfs://user-clicks/yyyy/mm/dd path for each days of data
received
Fields: Timestamp, userID,pageId, attributes
FileFormat: Parquet

Dataset2: User profile database snapshot stored in HDFS. Assume this company has 100's of millions
users. Stored in hdfs://edw/user-profile
Fields: userID (unique),country, state, city, ...
File Format: CSV

Using the above two datasets as inputs write distributed map reduce algorithm (pseudo code is fine)
to produce a daily report as below:

Average number of clicks to user ratio (#of cl in descending order of click ratio
Example output:
-----------+--------------
Country    |  click ratio
-----------+--------------
USA        |     8.0
-----------+--------------
CAN        |     7.2
-----------+--------------
...

You need to write this in simple map reduce algorithm, preferably in Java Map Reduce.
You may use pseudo code if you are not familiar with Java Map Reduce.
-----------------------------------------------------------------------------

 */
Job1:
    map(key:line,,,, value: ):
        userId -> 89

    reduce(key: userID)
        userID -> sum(counts) as clicks
        u1 -> 500
        u2 -> 123

    map2():  # dataset2
        userID -> raw_count  #  select  country, sum(clicks) from out1 join dataset2 using(userId)
        group by dataset2.country
        scan dataset2

    map3
        scan out2
        userID -> country

    reduce2(): # reducer is 1
        userId -> (sum_raw_counts, country)  # secondary sort on country (value).

        # in-mem country table (since there are only 200-odd countries);
        country -> sum(clicks), sum(1)

        # Q) How to do secondary sort among values?
        # in cleanup stage (reducers have it) emit the table order by ratio (this is how to do
        secondary sort on values)
        # with this optimization, downstream map4, reduce3, map5 and reduce5 can be avoided.
        # Secondary key (the value column to secondary sort on) is only used during sorting
        # before the reduce() function. Its not used in the grouping comparator and partitioning
        # comparator, where only the primary (aka natural)  key from the
        composite(key + value sort-column) is used
        # Brilliant illustration at -
        # https://www.quora.com/What-is-secondary-sort-in-Hadoop-and-how-does-it-work

------------------------------------------------------------------------------------------------
    map4():
        country -> (sum_raw_counts, 1)
    reduce3():
        country, sum(clicks)/sum(1)  # out3

    map5():  #scan out3
        # identity mapper
        # K-V
    reduce5():
        country -> V oder by V desc


     # total number of  clicks in country / total number of unique users in country

------------------------------------------------------------------------------------------------
Notes from illustration at
https://www.quora.com/What-is-secondary-sort-in-Hadoop-and-how-does-it-work

Stages in a map-reduce job -
1) Input phase:
    a) Creates split using InputFormat.getSplits()
    b) Read split (this is also part of the map-phase) using RecordReader

2) Map phase:
    a) Read split using RecordReader.nextKeyValue
    b) map function defined by implementing Mapper.map interface -> emits k,v
    c) Partition using Partitioner.getPartition to logically funnel map O/P to reducer.
        emits k, list(v)

3) Reduce phase:
    a) Reducer.reduce
    b) RecordWriter.write to write output to sink (HDFS, HBase, etc)
-------
Partitioning, sorting and grouping settings and key utilization -
Assume for the sake of below discussion that last_name is natural key and first_name is secondary
key to sort the value column on.

In the partition (last stage of mapper-phase), partitioning (hash vs range) of keys happens first,
followed by sorting of natural key and then secondary sort of value column specified (if any)
for the same natural key,
and then grouping of keys before pushing to reducer.

1) Partitioner class is mapred.partitioner.class aka JobConf.setPartitionerClass
    Only uses natural key for partitioning, so that they all go to the same reducer. Default is
    hash-partitioning, but can be also changed to range partitioning or another custom impl.

2) Sort: RawComparator mapred.output.key.comparator.class aka JobConf.setOutputKeyComparatorClass
    The output key comparator sorts using the entire composite key.

3) Group: RawComparator mapred.output.value.groupfn.class aka
    JobConf.setOutputValueGroupingComparator
    The output value grouping compares the natural key, ignoring the secondary sort key.

------------------------------------------------------------------------------------------------
Some related notes:
1) If you write Map-Reduce jobs like above, Cascalog will save you a lot of time and effort and
boilerplate.

2) Cascalog, is a Clojure DSL for writing Map-Reduce jobs very quickly and compactly.

2) Clojure is built for processing collections, which is great if you're working with a lot of data.
Clojure is designed for concurrency.

TODO: watch Rich Hickey's talk - Clojure creator, on philosophy behind the language -
http://www.youtube.com/watch?v=f84n5oFoZBc

Examples of what you can do with Clojure -
http://christophermaier.name/blog/2011/07/17/creating-a-query-dsl-using-clojure-and-mongodb

http://sqlkorma.com/
------------------------------------------------------------------------------------------------
MEANING OF A FEW MAPRED-SITE.XML PROPERTIES -

1) mapreduce.input.fileinputformat.split.maxsize = 256 MB

This is used in calculating split_size with the following formula

split_size = max(mapred.min.split.size, min(mapred.max.split.size, dfs.block.size))

In Amazon EMR, dfs.block.size = 128 MB (http://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-hdfs-config.html)

split size=max(default,min(256 MB, 128 MB))

So if split_size  = 256 MB, each map will process 1 split of 256 MB, ie 2 * 128 MB dfs_blocks on Amazon EMR.

Thumb_rule: mapreduce.input.fileinputformat.split.minsize < dfs.blocksize < mapreduce.input.fileinputformat.split.maxsize

Recommendation: 105 MB (minsize) and 270 MB (maxsize)

------
2) "mapreduce.job.reduce.slowstart.completedmaps" = 0.95
This setting controls what percentage of maps should be complete before a reducer is started. By default, we set this
to .80 (or 80%). For some jobs, it may be better to set this higher or lower. The two factors to consider are:

how much data will each reducer get
how long each remaining map will take
If the map output is significant, it is generally recommended that reducers start earlier so that they have a head
start processing. If the maps tasks do not produce a lot of data, then it is generally recommended that reducers start
later. A good rough number is to look at the shuffle time for the first reduce to fire off after all the maps are
finished. That will represent the time that the reducer takes to get map output. So ideally, reducers will fire off
(last map) - (shuffle time).
---------
Resources:
very useful: https://github.com/linkedin/dr-elephant/wiki/Tuning-Tips

This is also more comprehensive and useful -
http://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html#Task_Execution__Environment
------------------------------------------------------------------------------------------------

"""