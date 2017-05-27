# -*- coding: utf-8 -*-
"""
Answer on Quora to question -
Is HDFS way behind GFS (google file system)? If so, how?
https://www.quora.com/Is-HDFS-way-behind-GFS-If-yes-how-so

Google has a next-generation cluster-level file system called "COLOSSUS" that builds upon
the original version of GFS that appeared in 2009 in Jeff Dean's LADIS talk.
http://www.cs.cornell.edu/projects/ladis2009/talks/dean-keynote-ladis2009.pdf

--------------------------------------------------------
Storage Software: Colossus ( next-gen cluster-level file system) - vs HDFS
1) Automatically sharded metadata layer - HDFS has a related concept of a HDFS federation that
    allows multiple namespaces, each powered by a different NameNode, to co-exist on the same set
    of DataNodes. But its upto the admin to ensure that metadata in any given namespace doesnt
    exceed memory in the NameNode

2) Data typically writen using Reed-Solomon (1.5X) - Reed-solomon error codes that provide 1.5X
    redundancy help reduce disk usage while protecting data integrity by using parity bits to
    protect against corruption. Facebook has been working on building this into HDFS Raid since 2010
    but it remains an open issue for HDFS.

3) Client driven replication and encoding - Colossus's ability to replicate blocks across different
    clusters for geographic redundancy is something else that HDFS has yet to support. This is
    different from just having a single NameNode communicate to DataNodes in different geographic
    regions because HDFS clusters assume locality for performance.

Why Reed-solomon?
    a) Cost. Especially w/ cross cluster replication.
    b) Field data and simulations show improved MTTF
    c) More flexible cost vs availability choices
--------------------------------------------------------
Google's spanner has unified all data centers as one storage and computational unit since 2009 or
2010. With spanner, google's storage system has grown to a scale where it essentially treats an
entire data center, rather than an individual machine, as the basic building block. Spanner can
automatically scale resources and replicas based on usage patterns, network bandwidth and other
constraints. Autoscaling of resources happens across entire fleets of machines.

Open source Apache projects like HDFS and HBase are making good progress at becoming extremely
useful to companies at non-Google scale by providing similar systems, but they're definitely behind.

"""