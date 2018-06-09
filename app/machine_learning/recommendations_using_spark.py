"""
Optimizing recommendation pipelines using Apache Spark at Netflix
- Hua Jiang
Meetup on May 25, 2017

Offline experiment Design -> Collect label dataset ->  offline feature generation
-> Model training -> compute validation metrics -> model testing

If offline good, deploy online for A/B testing.

How to obtain features for offline training?
1) Viewing History Service
2) MyList Service
3) Thumbs Rating Service

Feed facts into feature generator -> Features -> Predictor -> Recommendations

Log features into hive tables. Comes with pros and cons -
Pros: No need to compute offline
Cons: delayed iteration for new features.

Fact logging + offline feature generation.
Pros: fast to add new features
Cons: need to rewind time and generate features
  Our time machine: DeLorean
  Tech blog: Distributed time travel for feature generation

Data snapshots in spark run once a day. Queries S3 for user sets based on different
stratification strategy. Thru Prana (Netflix OSS)

Feature encoders - transform raw data into feature numbers.

How to ensure parity of features generated offline and online?
Disparity => metrics become bogus.

Ans) RDD to data frame resulted in 3X run time gain in feature generation
from 2.5-3.5 hoursto 45-75 mins
Even if the new DataFrame created from RDD[Row] has columns with the same names,
they are different to Spark as they got transformed to RDD under the hood and TX to

new data frame.Manipulations on row objects are completely opaque, blocking optimizer
 from moving operations around.

 Version3 - column operations to the rescue.


If you dont have in-built function, then go for UDF.
Cons of UDF - Data encoding/decoding required.

UDF is usually written as a lambda function, input is a primitive and output is a primitive.

User-Defined Catalyst Expressions  - Flexible. User defines the operations.
Efficient because it uses internal data structure, so code generation possible.
Your expression has to be written on top of tungsten.

S3 -> Catalyst expressions -> Filtered Data Frame -> Feature Extractor

JSON Scan -> Filter
2X runtime gain compared to version 2. Now 25-40 mins for feature generation.
50~80 executors, 3 cores per executor.
------------------------------------------------------------------------------------------------
GENERAL NOTES BELOW ABOUT RECOMMENDATION SYSTEMS DESIGN-

1) https://xamat.github.io//pubs/BigAndPersonal.pdf
Data and Models behind netflix recommendations

"""