"""
Nov 6, 2020
https://www.youtube.com/watch?v=C-qo-SQoJug&feature=youtu.be
Reimagining Real Time Analytics in the Cloud - rockset

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

