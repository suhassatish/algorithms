"""
Hbase provides strong consistency guarantees at the cost of high availability.
As a trade-off, cassandra provides high availability at the cost of eventual consistency.

https://hortonworks.com/blog/apache-hbase-region-splitting-and-merging/
In hbase, a table is split into chunks of rows called regions. A set of regions are served by a
region-server (RS). Each region is served by only one RS. So if the RS goes down, that region
temporarily becomes unavilable until the RS comes back online. When a table is first created, by
default, only 1 region is created for that table. This means, irrespective of the number of RSes,
all requests initially go to only the 1st RS. Hence, initial data load cannot make use of the
whole capacity of the cluster.

Since its range-partitioning in the key-space, hbase provides tools for pre-splitting the table into
regions. This ensures initial load is more evenly distributed in the cluster. But data skew can
still exist leading to decreased cluster performance. No optimal number for number of splits, but
you can start with lower multiple of number of RSes and then let auto-splitting take over.
There are 2 in-built pluggable split algorithms - HexStringSplit and UniformSplit - exposed by the
RegionSplitter utility HexStringSplit is useful if there are hashes for keys.

HBase uses ZooKeeper to store some metadata for operations (master address, table locks,
recovery state, etc). Hbase keeps its data files as well as WAL (write-ahead logs) on HDFS or any
configurable file-system.

When a region reaches a size of 10 GB (default), it auto-splits into 2 regions of equal size.
The split policy uses the formula min(R^2 * hbase.hregion.memstore.flush.size, hbase.hregion.max.filesize)
where R is the max number of regions of a table managed by 1 RS.
hbase.hregion.memstore.flush.size default value is 128 MB. So the first region on RS will be split
at the first flush at 128 MB. As number of regions hosted on a RS increase, it will use increasing
split sizes. 512 MB, 1152 MB, 2 GB, 3.2 GB, 4.6 GB, 6.2 GB, 10 GB, 10 GB, 10 GB, ...

Split point is the midpoint in the block index for the largest store file in the largest store.
----------------------------------------
WRITE PATH IN HBASE -
1) Write requests are handled by the Region-Server. They accumulate in an in-memory data store,
called "memstore". When the memstore fills, its written to disk as an additional "store file".

2) As "store files" increase, the RegionServer will "compact" them into combined larger files.
Compaction is an expensive process as data files are re-written.

2.5) The Write-Ahead Log (WAL) records all changes to data in HBase to file-based storage.
Under norml operations, the WAL is not needed as data changes move from MemStore to StoreFiles.
However, if RegionServer crashes before the MemStore is flushed, WAL ensures changes to the data can
be replayed. If writing to the WAL fails, entire operation to modify the data fails. When a RS get a
DELETE() or PUT() request, it first updates the WAL, then the MemStore. WAL resides on HDFS at
/hbase/WALs/
WALs allow databases to do updates in-place. Another way to implement atomic-updates is
SHADOW PAGING, which is not in-place. Main advantage of doing in-place updates is that it reduces
the need to modify indexes and block lists. File systems use a variant of WAL for FS metadata,
called JOURNALLING.

3) After each flush or compaction finishes, RegionSplitPolicy decides if a region has to be split or
not.

4) When a split happens, the child will not rewrite the data, it will just create RefLinks to split
boundary. Although splitting decision is made locally at a region-server, it has to co-ordinate
with many actors. Below section describes it in detail.
-----------------------------------------
http://hadoop-hbase.blogspot.com/2012/03/acid-in-hbase.html
THE HIGHLEVEL FLOW OF A WRITE TRANSACTION IN HBASE LOOKS LIKE THIS:

1) lock the row(s), to guard against concurrent writes to the same row(s)
2) retrieve the current writenumber
3) apply changes to the WAL (Write Ahead Log)
4) apply the changes to the Memstore (using the acquired writenumber to tag the KeyValues)
5) commit the transaction, i.e. attempt to roll the Readpoint forward to the acquired Writenumber.
6) unlock the row(s)

THE HIGHLEVEL FLOW OF A READ TRANSACTION LOOKS LIKE THIS:
1) open the scanner
2) get the current readpoint
3) filter all scanned KeyValues with memstore timestamp > the readpoint
4) close the scanner (this is initiated by the client)
In reality it is a bit more complicated, but this is enough to illustrate the point.
Note that a reader acquires no locks at all, but we still get all of ACID.


ACID in Hbase
Key point: All transactions are committed serially.
1) Transaction in HBase means setting the current ReadPoint to the transaction's WriteNumber,
and hence make its changes visible to all new Scans.

2) The readpoint is rolled forward even if the transaction failed in order to not stall later
transactions that waiting to be committed (since this is all in the same process, that just mean
the roll forward happens in a Java finally block).

3) When updates are written to the WAL a single record is created for the all changes.
There is no separate commit record.

4) When a RegionServer crashes, all in flight transaction are eventually replayed on another
RegionServer if the WAL record was written completely or discarded otherwise.

------------------------------------------
TODO - http://hbase.apache.org/book.html#arch.timelineconsistent.reads
Best resource for Hbase internals ebook.

"""