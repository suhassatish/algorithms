"""
APACHE DRUID

white papers -
https://go.imply.io/Introducing-Apache-Druid-WP_LP.html
https://go.imply.io/WP-Fast-Path-to-Druid-Success-Registration.html
https://go.imply.io/WP-Real-Time-Analytics-from-Your-Data-Lake_LP.html

https://www.youtube.com/watch?v=id2_T9mEpR4&feature=youtu.be
How Netflix Uses Druid in real-time to ensue a high quality streaming experience
Sept 2020 - 2nd Druid Summit

https://www.youtube.com/watch?v=QZUunUDQ8p4&feature=youtu.be
how Druid powers real-time analytics at British Telecom - April 2020

https://www.youtube.com/watch?v=smo2aJbhthA&feature=youtu.be
analytics over Terabytes of Data at Twitter using Apache Druid - April 2020

************************************************************************************************************************
Nov 6, 2020
https://www.youtube.com/watch?v=C-qo-SQoJug&feature=youtu.be
Reimagining Real Time Analytics in the Cloud - ROCKSET

Arch diagrams at - ~/Dropbox/tech_extras/distributed_systems_big_data/rockset-real-time-DB/

Locally attached SSDs = hot storage for real-time index, rocksDB cloud-based

Tailer stores it in a specific protobuf format.

RocksDB cloud has remote compaction. CPU for keeping indexes online.

Virtual instances are used for querying.

Private VPC deployment option - data plane and control plane segregated.
Data plane has query, data paths.
Control plane has metrics, monitoring and orchestration that runs in rocksDB cloud

AWS' Private VPC link in AWS connects data and control plane.

"""

