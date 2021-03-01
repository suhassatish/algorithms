# -*- coding: utf-8 -*-
"""
http://www.cs.cornell.edu/projects/ladis2009/talks/dean-keynote-ladis2009.pdf
Notes from above LADIS talk by Jeff Dean -
One sever:
    DRAM: 16 GB, 100ns, 20GB/s
    Disk: 2 TB, 10 ms, 200MB/s

Local rack (80 servers):
    DRAM: 1 TB, 300 μs, 100 MB/s
    Disk: 160 TB, 11 ms, 100MB/s

Cluster (30+ racks):
    DRAM: 30 TB, 500 μs, 10 MB/s
    Disk: 4.8 PB, 12 ms, 10 MB/s

GFS usage @ Google:
200+ clusters
Many clusters of 1000s of machines
Pools of 1000s of clients
4+ PB filesystem
40 GBps read/write load in the presence of HW failures
Multiple datacenters, all around the World. A web search touches 50+ separate services, 1000s of
machines

Storage heirarchy: Local DRAM -> Local Disk -> Rack DRAM -> Rack Disk -> Datacenter DRAM
-> Datacenter Disk

Typical yearly flakiness metrics:
    1-5% of your disk drives will die
    Servers will crash at least twice (2-4% failure rate)
-----------------------
Typical first year for a new cluster:
~0.5 overheating (power down most machines in <5 mins, ~1-2 days to recover)
~1 PDU failure (~500-1000 machines suddenly disappear, ~6 hours to come back)
~1 rack-move (plenty of warning, ~500-1000 machines powered down, ~6 hours)
~1 network rewiring (rolling ~5% of machines down over 2-day span)
~20 rack failures (40-80 machines instantly disappear, 1-6 hours to get back)
~5 racks go wonky (40-80 machines see 50% packetloss)
~8 network maintenances (4 might cause ~30-minute random connectivity losses)
~12 router reloads (takes out DNS and external vips for a couple minutes)
~3 router failures (have to immediately pull traffic for an hour)
~dozens of minor 30-second blips for dns
~1000 individual machine failures
~thousands of hard drive failures
slow disks, bad memory, misconfigured machines, flaky machines, etc.
Long distance links: wild dogs, sharks, dead horses, drunken hunters, etc.
-----------------------
GFS Design -
1) GFS Master (like NameNode) manages metadata of where data resides among chunk servers (DataNodes)
2) Data transfer happens directly between clients to chunkservers
3) Files broken into chunks of ~64MB
-----------------------
Micro-service architecture -
1) Simpler from SWE standpoint
2) Few dependencies, clearly specified using protocol buffers
3) Ability to run lots of experiments
-----------------------
PROTOCOL BUFFERS - Desirable features
1) Self-describing, multiple language support
2) Efficient to encode/decode (200+ MB/s), compact serialized form (uses variable-length encoding)
3) Same protobuf format also used to store data persistently (not just for RPC N/W communication)

eg - For server returning a search result encoded with protocol buffers-
message SearchResult {
    required int32 estimated_results = 1; // (1 is the tag number)
    optional string error_message = 2;
    repeated group Result = 3 {
        required float score = 4;
        required fixed64 docid = 5;
        optional message<WebResultDetails> = 6;
    }
}

4) Systems ignore protobuf tags they dont understand, but pass the information through
    => No need to upgrade intermediate servers

5) Even microservice specifications can be written in protobuf as follows -
service Search {
    rpc DoSearch(SearchRequest) returns (SearchResponse);
    rpc DoSnippets(SnippetRequest) returns (SnippetResponse);
    rpc Ping(EmptyMessage) returns (EmptyMessage) {
        protocol=udp;
    };
}

6) Compact in-memory representations
-----------------------
NUMBERS EVERYONE SHOULD KNOW:
Important skill: Ability to estimate performance of a system design without actually having to build
it. Best system could be simplest, easiest to extend, highest performance, etc

L1 cache reference 0.5 ns
Branch mis-predict 5 ns
L2 cache reference 7 ns
Mutex lock/unlock 25 ns
Main memory reference 100 ns
Compress 1K bytes with Zippy (snappy) 2,000 ns
Send 2K bytes over 1 Gbps network 177 ns (2016 => 45X faster than 2005)
Read 1 MB sequentially from memory 7,000 ns (13X faster)
Round trip within same datacenter 500,000 ns
Disk seek (spinning plater) 3,000,000 ns
Read 1 MB sequentially from SSD 123,000 ns (16X faster)
Read 1 MB sequentially from disk 1,000,000 ns (7X faster)
Send packet CA->Netherlands->CA 150,000,000 ns

Example back of the envelope calculation using above numbers:
Q) How long to generate google image search results page of 30 thumbnails?
A) Design 1: Read serially, thumbnail size on disk = 256KB images on the fly.
30 seeks * 10ms/seek + 30 * 256K / 30 MB/s = 560 ms
where 30 MB/s = to read sequentially from images on disk;

Design 2: Issue reads in parallel
10 ms/seek + 256KB / 30 MB/s (time to read 2 thumbnail image from disk) = 18 ms
Ignore variance, so really more like 30-60 ms, probably

Variations:
    Caching (single images? Whole sets of thumbnails?)
    Pre-computing thumbnails

Couple of trade-offs of core libraries-
zippy: encode @ 300 MB/s, decode @ 600 MB/s, 2-4X compression
gzip: encode @ 25 MB/s, decode @ 200 MB/s, 4-6X compression

Dont imagine unlikely potential needs that aren't really there. Identify common needs and address
them. Ensure your design works if scale changes by 10X or 20X, but the right solution for X often
not optimal for 100X
-----------------------
Interactive apps: Design for low latency
1) Aim for low avg times. (happy users)
2) 90%ile and 99%ile are also very important
3) Think about how much data you're shuffling around.
    eg- dozens of 1 MB RPCs per user request => latency will be lousy

4) Worry about variance
    Redundancy or timeouts can help bring in latency tail
5) Judicious use of caching can help
6) Use higher priorities for interactive requests
7) Parallelism helps
8) Make your apps do something reasonable even if not all is right
    Better to give users limited functionality than an error page
-----------------------
Add sufficient monitoring/status/debugging hooks:
Try to answer the question - if your system is mis-behaving, can you figure out why?

All servers:
1) Export HTML-based status pages for easy diagnosis
2) Export collection of K-V pairs via std interface (I/F). Monitoring systems periodically collect
    this from running servers
3) RPC subsystem collects sample of all requests, all error requests
    >0.0s, > 0.05s, > 0.1s, >0.5s, >1s, etc
4) Support for low-overhead online profiling
    a) CPU profiling b) memory profiling c) lock contention profiling
-----------------------
BIG TABLE SYSTEM STRUCTURE (ANALOGOUS TO HBASE):

Each web page url is represented as (row, column, timestamp) in big table. Each webpage has several
version, hence timestamps become critical.

1) Bigtable master - Performs metadata ops + load balancing
2) Bigtable tablet server - serves data
3) Big table sits on top of the lower level consisting of
    a) GFS - holds bigtable tablet data, logs
    b) Chubby lock service - holds metadata, handles master-election
    c) Cluster scheduling system - handles failover, monitoring

4) Eventual consistency model - writes to table in one cluster eventually appear in all configured
 replicas

5) Arbitrary code (co-processor code) runs next to each tablet in table. As tablets split/merge/move
 coprocessor code automatically splits/moves too
6) Calls across multiple rows automatically split into multiple parallelized RPCs

100+ google projects use bigtable including web crawling/indexing pipeline, orkut,
my search history, google maps/google earth
~500 BigTable clusters. Largest cluster: 70+ PB data, sustained 10M ops/sec; 30+ GB/s I/O
-----------------------
Example coprocessor uses-
1) Scalable metadata management for Colossus (next-gen GFS)
2) Distributed language model serving for machine translation system
3) Distributed query processing for full-text indexing support
4) Regular expression search support for code repository
-----------------------
Gmail uses a mixture of strong consistency storage engines and weakly-consistent storage engines.

a) Sending a message is a heavy-weight consistent operation (hence takes more time, as its
transactional, possibly with chubby locks).

b) Marking a message as read is asynchronous and can be eventually consistent
"""