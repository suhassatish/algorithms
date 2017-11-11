# -*- coding: utf-8 -*-
"""
The high-availability engineering of Amazon S3 is focused on get, put, list, and delete operations.
Because bucket operations work against a centralized, global resource space, it is not appropriate to create or delete
buckets on the high-availability code path of your application. It is better to create or delete buckets in a separate
initialization or setup routine that you run less often.
------------------
1) Buckets contain objects (key-value pairs). Nested folders are supported by adding / within the key like org/date,
but actually, everything is flat. Nesting is just a view.

2) After you upload the object, you cannot modify object metadata. The only way to modify object metadata is to make a
copy of the object and set the metadata.

3) If you anticipate that your workload against Amazon S3 will exceed 100 requests per second, follow the Amazon S3 key
naming guidelines for best performance.

4) If your workload routinely exceeds 100 PUT/LIST/DELETE reqs/s or more than 300 GET reqs/s,
can use Amazon CloudFront for perf optz. Reduces cost of S3 look-up.

5) A key prefixed by timestamp may go to the same partition and overwhelms the I/O capacity of the partition.
eg - This creates bad data skew - examplebucket/2013-26-05-15-00-01/cust1248473/photo7.jpg

    Randomness of the prefix more evenly distributes key names across multiple index partitions.

    28-08-1986/
    is a better date format for directory to partition evenly than 2016-08-28/
------------------
STORAGE CLASSES  -

1) STANDARD (default) - ideal for performance-sensitive use cases and frequently accessed data.
2) STANDARD_IA (infrequently accessed) - has separate retrieval fee. Available for real-time access.
3) GLACIER
------------------
VERSIONING -
If you have not enabled versioning, then Amazon S3 sets the version ID value to null.

Enabling and suspending versioning is done at the bucket level.
------------------------------------------------------------------------
OBJECT TAGGING -

1) Can add tags to existing objects or new ones.
2) Case sensitive keys & values

eg tags (can have multiple per object)-
Project=x
Classification=confidential
---------
eg 2 -
photos/photo1.jpg
project/projectx/document.pdf
project/projecty/document2.pdf

You can tag photo1 above in projectx category.
---------
1) Tags enable fine-grained ACL. Can grant IAM user permission.
2) Can combine tag-based filter in addition to key-name-prefix in an onject lifecycle rule.
3) Can customize Amazon CloudWatch metrics and AWS CloudTrail logs to show specific tags.
------------------------------------------------------------------------
Bucket and object permissions are independent of each other. An object does not inherit the permissions from its bucket.
 For example, if you create a bucket and grant write access to a user, you will not be able to access that user’s
 objects unless the user explicitly grants you access.

------------------------------------------------------------------------
syntax -
arn:partition:service:region:namespace:relative-id

For S3, you don't specify region and namespace.
example of bucket policy -
arn:aws:s3:::bucket_name
arn:aws:s3:::bucket_name/key_name
arn:aws:s3:::examplebucket/developers/design_info.doc

can use variables too
arn:aws:s3:::bucket_name/developers/${aws:username}/

"""

{
   "Version": "2012-10-17",
   "Statement": [
      {
         "Sid": "ExampleStatement1",
         "Effect": "Allow",
         "Principal": {
            "AWS": "arn:aws:iam::Account-ID:user/Dave"
         },
         "Action": [
            "s3:GetBucketLocation",
            "s3:ListBucket",
            "s3:GetObject"
         ],
         "Resource": [
            "arn:aws:s3:::examplebucket"
         ]
      }
   ]
}
#  Because this is a bucket policy, it includes the Principal  element, which specifies who gets the permission.
SELECT
  top(EventCode, 6)
  , count(*)
FROM [gdelt-bq:full.events]
WHERE Actor1CountryCode in ('DZA', 'AGO', 'ECU', 'GAB', 'IDN', 'IRN', 'IRQ', 'KWT', 'LBY', 'NGA', 'QAT', 'SAU', 'ARE',
  'VEN')
  and substr(EventCode, 2) in ('10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20')
  and Year > 2013;


SELECT
  Year
  , count(distinct GLOBALEVENTID)
  , avg(GoldsteinScale)
FROM [gdelt-bq:full.events]
WHERE Actor1CountryCode = 'IRQ'
 and substr(EventCode, 2) = '10' --demands
Group by 1
order by 1;
