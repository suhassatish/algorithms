"""
Given a search string like "the blue fox", return list of all document_ids
that contain the words "blue" and "fox"

Requirements -
1) Ignore stop words
2) Does order matter - do they need to be next to each other? No, they dont have
to be adjacent.
3) Storage of record does not matter, just retrieval

Services - single service
Data Model -
    document_id
    unique_words
Inverted index of word to [doc_ids, freq, etc]


Design constraints -
1) Latency - say 10 ms => single service will have a cache tier.
2) QPS - Thumb rule = 300K/s concurrent users.
3) How many documents? ~100 Billion
4) Avg number of unique words/document - Lets say about 1k unique words/document (not relevant)
Upper bound = total number of words in dictionary. 170k words in Oxford dict v2.

Lets say 200k * 100B = 20 PB of memory in worst case. This is unrealistic.

Avg number of documents per word = ? Lets say 10k
----------------------------------------------------------------
Cache tier - A cluster of cache servers. Then there will be routers/load balancers.
Cluster manager and config store.

What are the cache servers going to store?
The entire inverted index has to fit in the cache.

Partitioning/sharding the index?
Range partition to avoid skew. Number of words in lexicographical order/number of servers
= 200k/60 = 3k words per server

Config store contents -
[word0 - word3k] = shard0 = servers 1,3,5


Number of search terms = guaranteed parallelism in map stage.

But intersection of documents has to be done in the router which is the reduce stage
and becomes the bottleneck.

eg - 1M documents containing "blue" intersect 500 docs containing "fox"
Have to do like a merge sort for intersection to avoid O(N^2) computation
So its O(N lg N) in worst case. This has to happen even before the
user gets the 1st result back.

Whats an alternative approach for sharding?


Shard 100B documents across 60 servers.
Server 0 only keeps inverted index of documents 0-100B/60 , say 1st 2B docs
Then cosine similarity of query dot document_word_vector can be parallelized.
So there is no reduce step here.

Cons - Extra memory usage, network bottle-neck for data transfer

Lot more replicas required to serve such systems.
Since they're static systems, replication is not a  problem.
So they replicate heavily to distribute the work in parallel.


To give the best user experience, you have to remove the reduce bottle-neck.


word-based sharding or doc-based sharding - which is better for writes and why?
eg - to update index when a document is updated.

answer - Only document[2.5B] needs to be updated which is sure to sit on 1 machine.

In word based partitioning, all machines with words in the document have to be updated.
This becomes a 2-phase commit, kind of transaction. Which is an eventual consistency model.
The "fox" machine has to update its inverted index of documents containing that word,
the "blue" guy needs to update its inverted index, then both prepare to commit and send out
a timestamp.
Then the master sends ack of highest timestamp it received and sends it back to the 2 servers.
If the local timestamp > (A or B) , then C = new timestamp thats sync-d. This is called 2-phase
commit protocol. Paxos or raft use similar 2-phase commit approach.

"""