"""
Design a twitter application, then drill down on news feed feature design.

Functional requirements -
1) User account management
2) publish a tweet
3) follow/unfollow users
4) timeline of tweets from your network
5) see notifications
6) endorse a tweet - `like`, `comment`, etc
7) analytics -  hash tags, trending topics
8) search & hash tag retrieval service

Services -
1) account management service
2) tweet ingestion service
3) social graph service
4) news feed/timeline service
5) notification service
6) endorsement service
------------------------------------------------------------------------------------
Data model per service -
1) account management service
    user_id (primary key) (8B)
    characteristics associated with a single user
    total followers (8B)
    total followees (8B)
    say 1 row = 1 KB

2) tweet ingestion service
    tweet_id (primary key)
    text (aka payload), or pointer to image, video, etc (metadata-only)
    timestamp
    retweets
    stats - `likes`. But can't put nested comments here in single record
    [hash_tag_ids] - allow limited, only 10. If million hash tags can be stored per tweet,
    then it has to be a separate service

3) social graph service
    follower : user_id
    followee : user_id

4/5 - can reuse above data

6) endorsement service (likes, comments) -
    endorsement_id
    tweet_id
    endorser user_id
    type (like, comment)
    payload
    timestamp

7) retweet
    retweet_id
    original tweet_id
    user_id performing retweet
    timestamp

8) search & hash tag retrieval service
    tag_id
    tag_string
    array of original tweet ids (distributed hash map)

------------------------------------------------------------------------------------
Design constraints - Capacity & compute -

1) users
Say there are about 400 M users.
400 M users * 1 KB/users table row = 400 GB
But a row will be only about 1/3 KB, so maybe 100 GB is enough
=> single node is good enough. Could be mysql. No need to be distributed

2) tweet ingestion service
payload = tweet = 140 characters = 140 B * 6k tweets/second * 86400 s/day * 365 days/yr
 = 140B * 189B tweets/yr
Assume 300 Bytes per tweet row * 200 Billion tweets/yr, for 3 years,
 300 bytes * 600 Billion tweets in 3 years = 180 TB ;
can be served by a single server; 1 commodity server usually has 100 TBs of storage;
Storage is cheap ~10 cents/GB => $100/TB => $10k/100 TB

6K/s ingestion, takes 10ms to write a tweet into the DB.

3) social graph - 400M * avg 50 followers/user = 20B rows * size per row (assume 20 bytes) = 300 GB
  capacity-wise does not require a distributed system.

What about QPS of a distributed system? Reads are much more intensive for timeline queries.
follower-followee entity will be poked by timeline query.

4) timeline service - does not have a source of truth tier. Whats the QPS?
Maximum number of concurrent users at peak hour = 300K/sec, thumb rule is few hundred Ks per second

Latency of a timeline query - sub-second ~10ms.
A server gives you 100 parallel conxns,
 each is 100 req/10ms => 10k req/s

 10k/sec if you saturate all CPUs.
If CPU util = 50%, 5k requests/sec QPS is what a server is able to generate.

50-60 servers for read traffic.

60 servers * 5k requests/server/s = 300K/sec
------------------------------------------------------------------------------------
Timeline service design-

Does not require a source of truth.
Data model in Cache tier -
    recent tweets of people in your N/W.

    For each member A:
        for each person B that A follows:
            select most recent tweets by B and cache 100 of them, and paginate.

100 tweets/member * 400 M members to be kept in memory. Need to have a larger number of servers
since each server has lesser memory than storage (disk).

16 GB/1 TB = 1.6 TB memory/100 TBs per server.

1 TB/16 GB = 60 times more disk than memory is available on a server.
------------------------------------------------------------------------------------
Push-pull model for event service refresh of timeline -

100% Push-model:
    Pros - When a tweet is generated, it is pushed to the timeline service for all followers.
    Consistency. Read latency

    Cons - Write latency, burst of traffic on fanout

100% Pull-model:
    Pros - When a user logs in, timeline service query for the user is generated on-demand.
    Write latency.

    Cons - Read latency is much higher if you want consistent reads.
    Timeline service will be very slow.

Hybrid approach - LRU caching of frequent users' timelines being cached.
Twitter allows upto 5s of staleness per data center geographic region.
------------------------------------------------------------------------------------
References -
1) https://www.quora.com/What-are-the-scaling-issues-to-keep-in-mind-while-developing-a-social-network-feed
2) https://www.quora.com/Software-Engineering-Best-Practices/What-are-the-best-practices-for-building-something-like-a-news-feed
3) http://highscalability.com/blog/2013/7/8/the-architecture-twitter-uses-to-deal-with-150m-active-users.html
"""
