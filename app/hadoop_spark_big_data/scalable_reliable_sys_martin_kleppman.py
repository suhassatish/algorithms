"""
Notes from Martin Kleppmann's book - Big Ideas Behind Reliable, Scalable, Maintainable Systems
----------------------------------------------------------------------------------------------------
Chapter 3 - Storage and Retrieval -

Indexes - Indexes slow down writes as the in-mem index also has to be updated with every write. The
simplest write is an append-only log. Trade-off: Well chosen indexes speed-up reads, but slow down
writes.

A) Hash-indexes:
    a) Keep an in-mem hash map of {key: byte_offset} to data file on disk where the values
of columns for that key can be found. This is what BitCask - the default storage engine in Riak
does.

    b) It offers extremely fast reads subject to the fact that all the keys fit in-memory. The value
can be fetched from disk with just 1 disk seek. If that part of data file is already in filesystem
cache, it doesnt need any disk I/O at all.

    c) Eg app - key = url of cat videos, value = Number of clicks/views. Limited number of cat
    videos on internet, but each one can be viewed millions of times. Large number of writes per key

    d) Since its append-only log, how to ensure we dont run out of disk space? Soln: Keep segment
    files and close them when they reach certain size, and then allow for compaction s.t. duplicate
    keys only retain the most recent value. Start a new segment file when each previous one reaches
    say 1 GB on disk. Can perform compaction and file_segment merging simultaneously.
-----------
    Implementation Considerations:
    i) Crash recovery - Persist in-mem hash_map on disk and re-load it upon DB server restart. Each
    segment-file has 1 in-mem hash_map. Single bg thread does segment compact & merge writing to
    new compacted_segment_file while old segment continues to serve reads. Once done, new becomes
    primary and old segment is deleted.

    ii) Data formats - CSV is storage inefficient compared to binary.

    iii) Deleting records - Not done in-place. Keep a tombstone dirty bit, and during compaction,
    all values of deleted key are thrown away.

    iv) Partially written records: DB may crash at anytime. Maintain checksum for each value,
    allowing corrupted parts of log to be detected and ignored.

    v) Concurrency control: Segment files have single writer thread and multiple reader threads.
    Segment file is immutable, append-only log. Append and segment-merge are sequential write ops,
    hence much faster than random WR.
----------------------
B) SSTables and LSM-Trees: SSTable stands for sorted-string table. Keys in log-file are sorted. Keys
in in-mem index are also sorted, but not all keys are in index (sparse).

    a) Since segment files are timestamp-ordered, when same key is contained in multiple segment log
    files, we keep the value from the most recent segment-file for that key. Adv: Merging
    segment-files reduces to O(n)-time operation (from O(n lg n)) since keys within each file are
    sorted.

    b) All keys dont have to be kept in in-mem index. Only 1 key for a few KBs on disk is enough,
    since KBs of sequential-RD is very fast. Eg - key1 = handbag, key2 = handsome exist in index;
    If searching (RD) index for handiwork, only a sequential disk log scan between the value-offsets
    for keys b/w handbag and handsome is sufficient.

    c) Groups of values between consecutive index-keys can be compressed before writing to disk.
    Compression saves disk space as well as reduces disk I/O B/W.

    d) If all keys and values were of same size (which is rarely the case), no need in-mem index at
    all. Can just do binary search on append-only SSTable log segment file. But since variable-len
    columns are more common in practice, cannot know the exact end-point of a row before runtime seq
    RD-access.
-----------
    Constructing and maintaining SSTables:
    a) Maintaining a sorted-tree structure on-disk is possible. In-mem is even easier
    with AVL or red-black (balanced) BSTs.

    b) WR-RD patterns:
        i) When a WR comes in, add it to in-mem red-black BST index. This index is sometimes called
        memtable.

        ii) When memtable_size > threshold (~10s of MBs), write it to disk SSTable file. New SSTable
        file becomes most recent segment of the DB. While SSTable is being written-to on-disk,
        memtable can accept new writes.

        iii) To serve RD request, 1st search in memtable, then in most-recent SSTable segment, then
        in next most recent, and so on.

        iv) If DB server node crashes, memtable recent-updates are lost. To prevent this, maintain
        a write-ahead log (WAL) persisted on-disk and parallel writes to both memtable and WAL.
        Then can replay from WAL upon DB-server-node-failure and update SSTable.
-----------
    Making an LSM-tree (log structured merge) out of SSTables:
    Basic idea of LSM trees: Keeping a cascade of SSTables that are merged in the bg.

    Advantage:
    1) Even when dataset is much larger than available memory, continues to work well.
    2) Efficient read queries due to sorted keys & hence range key-search.
    3) Very high WR thruput due to append-only logs into bst-in_mem index and b-tree type on-disk
    SSTable sorted log file.

    (This algorithm is used in LevelDB and RocksDB - K-V storage engine libs designed to be embedded
    into other apps).

    i) LevelDB can be used in Riak instead of Bitcask. Similar storage engines are used in HBase and
    Cassandra, both inspired by Google's BigTable paper.

    ii) Lucene, an indexing engine for full-text search used by Elasticsearch and Solr uses a
    similar method for storing its term-dictionary. Full-text index is similar in idea, but more
    complex than K-V index. Key = word, values = [list of doc_ids]. In lucene, this mapping is kept in
    SSTable-like sorted files.
-----------
    Performance optimizations:
    1) Searching for key that doesn't exist can be slow. Memtable look-up, followed by SSTable files
    scan from newest to oldest before detecting a KeyDoesntExist condition.

    2) To optimize for this, memory-efficient bloom filters are used, that can approximate the
    contents of a set. Saves many unnecessary disk reads for non-existent keys.

    3) Determining order and timing of SStable merge & compactions: Size-tiered (HBase) vs
    leveled (levelDB) compaction. Cassandra supports both. In leveled compaction, key-range is split
    into smaller SSTables and older data is tenured into separate levels.
    Advantage: Incremental compaction using lesser disk space.
----------------------
C) B-trees
    1) Difference with SSTables & LSM-trees: Break the DB down into fixed-size blocks or 'pages',
    usually 4KB in size, whereas SSTables are variable-size segments.

    2) B-trees use pointers to address locations on-disk. Look-ups start at root of b-tree.

    3) Number of references to child-pages in 1-page of a b-tree is called 'branching factor'.

    4) New key insertions: Go into b-tree page which contains the range around that key. If page
    doesn't have enough space to insert new key, it splits into 2 half-sized pages and key gets
    inserted into 1 of the new pages.

    5) B-tree with n nodes always has a depth of log(n). Most DBs fit into a b-tree of 3-4 levels
    deep. 4-level b-tree of 4KB pages with branching factor of 500 can store upto 256TB of data.

    6) B-tree values are updated in-place, in stark contrast to append-only SSTables & LSMs.

    7) B+ tree optimization: Save space in pages by abbreviating the key in a deeper level than
    storing the full key. Keys only need to contain enough info about range boundaries. This results
    in higher branching factors.

    8) Optimization: Instead of modifying pages on updates, copy-on-write can be adopted for
    concurrency control and snapshot isolation, along with WAL for crash-recovery. Modified page is
    written to new location and new version of parent page is created pointing to new location.
----------------------
D) Comparing B-trees vs LSM trees: Generally LSM trees are faster for writes whereas B-trees are
faster for reads.

Advantages of LSM-trees
    1) A B-tree index must write every piece of data twice, once to the WAL and another to the
    B-tree page itself. Even if only a few bytes in the page changed, have to write an entire page
    at a time. Some storage engines overwrite the same page twice to ensure no partially updated
    pages exist upon power failure.

    2)
    Log-structured indexes also need to write multiple times to disk due to repeated compaction and
    merging of SSTables for every WR to DB. This is called write amplification. Its of particular
    concern on SSDs where blocks of data can be over-written only a fixed number of times before
    wearing out.

    3)
    In WR-heavy apps, perf bottleneck can be the rate at which DB can write to disk. More a storage
    engine writes to disk, fewer WR/s it can accept in the available disk B/W.

    4)
    On magnetic hard-drives where seq-WR is much faster than random-WR, LSM trees have advantage of
    higher WR thruput.

    5) LSM-trees can be compressed better on-disk.

Disadvantages of LSM-trees
----------------------------------------------------------------------------------------------------
MySQL InnoDB storage engine - In-mem K-V index where value is not just pointer address to actual
location of data on disk (called heap file). That is too much of perf penalty for RDs. Desirable
to store the whole row directly within an index. This is known as clustered index. In InnoDB,
primary key is always a clustered_index. Secondary index refers to the primary key instead of heap
file location. In SQL Server, can specify 1 clustered index per table.

A compromise between a clustered index (storing all row data within the index) and
a nonclustered index (storing only references to the data within the index) is known
as a covering index or index with included columns, which stores some of a table's columns
within the index [33]. This allows some queries to be answered by using the
index alone (in which case, the index is said to cover the query).

The most common type of multi-column index is called a concatenated index, which
simply combines several fields into one key by appending one column to another (the
index definition specifies in which order the fields are concatenated). eg - telephone directory
LN, FN. Useless if you want to find everyone with the same FN. Appln - geospatial data

SELECT *
FROM restaurants
WHERE latitude > 51.4946 AND latitude < 51.5079
    AND longitude > -0.1162 AND longitude < -0.1004;
PostGIS implements geospatial indexes as R-trees using PostgreSQL's Generalized Search Tree indexing
facility.
------
Full-text search and fuzzy indexes - In lucene, spelling errors are ignored by index searching for
words within a levenshtein distance of 1, to be able to fuzzy-match.

In Lucene, the in-memory index is a finite state automaton over the characters in the keys, similar
to a trie.

"""