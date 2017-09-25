"""
Design a URL shortener service.

Need to hash a URL into a 6-digit hash.
--------------
What are the use cases or functional requirements of the problem?

1) Generate a short URL given an input long URL, and vice versa.

2) Different looking URLs that are actually symbolic-links should hash to the same page.

3) Provide expiration capability for link.

4) Ensure validity/uniqueness of URL, shouldn't be collision

5) You can run analytics on the URL like hit rate, click-through rate, etc
------------------------------------------
Map Functional Requirements to Services

1) A single URL shortener service. Lets make it a service.
Netflix has many services like payments, login, recommendations, etc

2) We'll then get data models for each service, or entity relationships.
unique_id|short_url|long_url|creation_time|expiration_time|statistics

----------------------------
Then ask for design constraints - 2 types
  a) Capacity constraints for storage - memory, disk
  b) Compute constraints - CPU, N/W, I/O

Upper bound on the number of URLs generated.
Size of each column - limit short URL , limit long URL.

If for short url, we use A-Za-z0-9, then we have 26*2 + 10 = 62 characters.
So 62^6 combinations = 56B URLs can be supported before there can be a hash collision.

-----
Compute constraints

1) Latency of operations - for a single operation, whats the end-to-end response time
A few milliseconds. Here something like P50 (median), P90, P95, P99 (percentile slowness)
Set service level agreements -  10ms, 40ms, 50ms - latency of writes
Latency of reads - retrieving. Must be lesser since there are more reads than writes. 1-5 ms.

SLA is usually for P50.

2) Throughput requirement - total number of operations per unit time
Write ops per second = Similar to number of tweets per second = 6k/sec
Read ops per second = On an avg, there can be 50 followers per user, so 6k * 50 = 300k/sec

Also known as QPS or queries per second
----------------
Amazon example:
5 PB - takes 3 days to move over truck.

10 MBps N/W B/W * 24*60*60 seconds/day = 864 GB per day => 5 * 10^6 GB / 864 GB per day = 5787 days
 = 15 years
Therefore, it takes only 3 days to move truck.
----------------
Capacity Estimation -
7 bytes for short_url + 100 bytes for long_url + 8 bytes for unique_id + timestamp,
~200 bytes/record (max)

number of records in a year = 190 B records/yr => takes 20 years to fill up. Reasonably long time

Number of bytes per year = 600 * 190 B = 120 TB per year
We should design a system that can handle load for atleast 3 years, so that I dont have to add nodes

360 TB.

Capacity on a single server = 100 TB, so you will need 4 servers.

Availability of 99.99%. We use 3-way replication = 360 * 3 = 1080 PB

Typically a single server (data) provides 100-200 number of concurrent connections (open ports)

Each thread can take an average of 15ms.
To avoid concurrency issues, 100-200/15 = 10-20 K ops/sec.

To utilize 50% of CPU utilization, 5k ops/sec/server is good.

To serve reads, you will need 50X times writes, you will need 60 servers minimum to support the read
QPS.
----------------
Design Template thats easy to apply in generic cases -
1) System is a set of one or more services
2) Each service is a set of tiers -
    application server tier that handles the application logic,
    cache server tier for fast reads, writes,
    source of truth/persistence tier
3) Each tier is a distributed system of its own depending on the capacity and compute estimations

4) It can start out as a single server, but scales over time and requirements
----------------
Distributed architecture template -

1) Cluster of servers that are dedicated to serve the tier

2) Distribution of data/workload across servers
    sharding/partitioning comes into play

3) Since there is distribution across a number of servers, will need routers or load balancers
    Routers route requests to correct dedicated server
    If requests are stateless, then load balancer is sufficient. Exposed as a single REST endpoint.

4) Cluster manager checks which of the dedicated servers are alive or dead - apache zookeeper
is a very popular cluster manager. Design a cluster manager is a popular question - you will have to
talk about split-brain problem - paxos algorithm (for consistency). Leader election.

5) Config manager - maintains metadata of which server hosts what. Its called control plane.
Given a request, where should it be sent? This information is provided to routers. Router can
cache that information.
----------------
Bottom-up approach -
How do you distribute the load of an incoming request
across a table in 60 servers? Range partitioning on unique_id
Config store contents:
0-1B = shard0=server 1,3,5
1-2B = shard1=server 2,4,6,... etc

Round-robin sequencing. Given a long URL, hash to a random shard_id, find the highest unique_id
on that shard. (each DB server can handle sequence)

Assign a long URL to the unique key and then
interviewkickstart.com -> shard_id=0 => value of 65 =
0*62^6 +0*62^5 +0*62^4 +0*62^3 +0*62^2 + 1* 62^1 + 3 -> aaaaabd

References -
1) https://www.quora.com/What-is-the-architecture-of-a-scalable-URL-shortener
2) https://blog.codinghorror.com/url-shortening-hashes-in-practice/
3) http://www.tkkader.com/2012/03/how-to-hire-a-hacker-for-your-startup/

"""