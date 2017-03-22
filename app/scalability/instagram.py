"""
Requirements:
1) Post a picture
2) Comment/share on a pic
3) follow
4) top instagrams in your feed
5) direct msg a user
6) search service
7) support multiple resolutions


database_schema:
pictures table:
    id
    filters_applied = [] # non-core metadata
    timestamp
    caption
    link_to_actual_img
    created_by (user_id)

why link_to_img vs BLOB of image within DB itself?
If you have BLOB in DB, if you're serving 1M concurrent users, each 4 MB image,
you'll hit read limitations.
So it makes it less scalable on the server side.

Trade-off: Image can be on amazon_S3://
Every user has their own bucket where they can upload images. Then you pass that link in the
request. Whats the drawback of this approach? You're vendor-locking-in to amazon.
Volume may become prohibitively explosive to store on S3.

To abstract cloud_provider and not incur the cloud storage cost, what would you do differently?
You delegate the responsibility of delegating to cloud service, to the server.
                                    _cloud_provider1 (amazon)
Client -> FileManagementService -> |
                                   |_ cloud_provider2 (rackspace)
This shields the client from sub-system evolution on the cloud_provider side.
---------------------------

Sorting while serving feed -

1) most-recent-first
facebook news feed is a big team in FB to improve user engagement.

id can be a concatenation of
|timestamp|shard_id|id|
Instagram uses 41 bits for the timestamp field, you can get 41 years of timestamps there.
shard_id is 13 bits. 2^13 = 8196 shards
id = 10-bit

Google has solved it with an atomic clock of their own. NTP gives you 10 ms SLA.
Lets assume its within that synchronization time and its acceptable.
---------------------------
If celebrity took a photo, what does Instagram do? Push notifications?
Event-based pub-sub architecture.

A popular user u1 may have 1M followers.
u1 post_photo_event -> service1 -> fanout_service -> for_each follower: batch & send_notification
                               |-> this communication has to be an asynchronus RPC call;
If its synchronous, it limits scalability on service1.
You want batch notifications.

how to make it asynchrnous? Ans: msg_queue and publish-subscribe
Fan-out service can do consolidation of notifications.
 u1-> f1, f2, fn
 u2 -> f2, f5

f1 => u1
f2 -> u1, u2

Notification handling service that gets these events.

You can have a cache of last logged-in users (LRU cache on Time-To-Live for monthly-active-users).
You can notify non-active users only when they login.
---------
there can be a feed service which marks a dirty bit in your queue saying there's an update.

feed service will accumulate new ordering of events and keep it ready for you.

where will a pull-service be useful?
if you have lots of friends, you dont want to get overwhelmed by notifications. thats when pull
comes in.
-------------
What are the top trending photos? Or top-events (view, react, share, like,etc are events)?
Generate top trending events in the last 1-hour. How to do it?

If you keep event_statistics in cache, bottleneck will be on write-throughput to increment the
counters.
Its a map-reduce problem ie for a photo_id, how many events (shares) occurred?

Service receives event (photo_id, user_id, etc).
You may have to write an importer with a pig script which will give you results.
Its intensive on the DB side.

You can avoid disk-overhead of M/R by using event-logging.
The service itself could write an event to kafka. A logging service could be a subscriber to this
topic and then write it to the loggingInfrastructure. Here you make an RPC call b/w pub-sub &
listener. Rely on SOA and externalize with micro-service model.

Or you could have a log forwarding service that flushes events. This has more moving parts.
-------------
Logically, events are an append log. Take the last 1 hr of log records and act on it, ie
run M/R jobs on it. Service like log-tailer. Can develop in-memory processing of this.
key           value
photo_id -> [likes, shares, ...]

top-k using quick-select (O(n)) or heap (O(n lg n)).

TODO: encourage you to read twitter's storm for M/R in-memory. This has evolved to heron.
Read heron. Also read about yahoo buzz feed.
-------------
Sticky sessions: Its when the client and server

client -> (session_id) -> server
{cookie}                  {cookie: tag}
If server1 having cookie info about user crashed, and this info is lost.
Now the shopping_cart of user is empty. Its bad user experience and costs amazon money.
Amazon server should not assume that a particular user always goes to a particular service instance
node. App load_balancer takes you to particular server based on session_id.
This is never a good design for server scalability.

HTTPS & sticky-sessions - In a highly encrypted multi-tenant environment, since servers
 communicate over non-HTTPS, a hackerService can snoop over the internal network.

IPSec and IPv6 tunnels are there to mitigate performance degradation and speed-up TLS hit over HTTPS

"""