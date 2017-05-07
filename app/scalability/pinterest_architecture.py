"""
John Elliott talk at AWS Summit- SF on April 19, 2017

150 PB of data in S3
80+ TB of new data/day
Almost entirely log data

Logging infra v2 -
Singer -> Kafka 0.8 -> Secor/Merced -> S3 sanitizer -> hadoop
real-time kafka consumers are storm, spark-streaming

Storage growth since 2014 Jan = 1467%
12 months = 86%
YTD = 60%

S3 data structure -
level 1 = bucket/
level2 = application/
level 3 = table_name/
level4 = dt = 2017-04-13
---------
old data flow - 6 hr runtime
S3 bucket listing -> inve job ->
|_> ops job        ->efficiency job -> efficiency report

new data flow = 20 min runtime
S3 analytics provides much needed data on object age and access patterns


"""