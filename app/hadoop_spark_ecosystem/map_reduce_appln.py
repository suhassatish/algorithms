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

"""