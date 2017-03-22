"""
For external component design, REST API is the norm.

Logical Architecture of most apps today:
Client (like uber app, FB app etc) <-> API <-> BizLogic <-> Persistent DataStore, ElasticSearch (ELK)

Murali 500Miles app tech stack -
iOS/Android WebApp; API + BizLogic in node.js; DS = MongoDB

Why is API layer crucial? To talk to multiple WebApp endpoints, REST API is the goto standard
now-a-days.

To access a service, you need to open a port on a firewall.
Challenge comes when an international traveler accesses services from different geographies.
In your office, ppl dont want you to connect over multiple protocols.
eg - TCP 24954 is probably a trojan?
So it will be shut off. Its very hard for services to be available across a variety of protocols
+ ports.

HTTP 80 + 443 (TLS) has hence become the standard.
HTTP status codes -
2XX => 200 = success
3XX  = modified; 302 = redirect; 304 = not modified;
HTTP is a universal standard thats interoperable across multiple devices.
Nothing on the API front needs to change when you make android, iOS, and other arbitrary platforms.
4XX = client-side errors => 403 = credentials-service when someone cleared the cache;
    404=page not found
5XX = server-side errors

Does API-layer have to be platform-agnostic or device-specific API-layer? What are the trade-offs?
Netflix has a device engineering team for various kinds of devices from ps3/gaming consoles to Tvs
to mobile phones to ipads.
Android has a very specific way of rendering graphics/resolutions. Specific resolutions go to
certain endpoints. eg - android image of medium resolution.
/android/img/?name=blah&format=xhdpi
only andoir devices can specify resolution parameter xhdpi.

API server becomes complicated if it has to handle device-specific details.
--------------------
Is ELK-stack common even for events?

Client1 & Client2 talking to TweetService
Client1: tweet: "weather is great today"
Client2: tweet: "hows the weather today?"

Client3: search: show me all weather-related tweets today?



Here ELK stack is very handy for search-indexing. Without it, you have to run non-trivial queries
across the DB. Lucene or SOLR what they do is they parse the tweet content and create hash-maps of
inverted indexes which look like this -
weather -> tweet_id1, tweet_id2
--------------
500Miles went with NoSQL for 2 reasons -
1) If you ask DBA which is more scalable? Its apples-to-oranges comparison.
NoSQL gives you patterns not to have complexity within the DB-layer.
It depends on the queries. 1 fine-day its fine, for complex queries, it may choke the DB.
2) With NoSQL, scaling the DB is trivial. You can focus on app-developers. You can say directly
off the bat that you can scale upto so many users.



How do MongoDB and ELK work together?
Get me all the companies, then get me all the jobs. There are 2 queries per request.
Some patterns to mitigate read-heavy traffic -  load balancer to read from read-only slaves.

This can be avoided by doing all work by reading of ELK servers.
For all visualizations about company insights, its specific data attributes of an entity.
This is look-up on particular company_id and hence, it queries MongoDB.
-------------
API team or business logic team can ask you REST API design questions.

For choice of programing language, REPL support is important (quick feedback loop).
Also, documentation and community support is very important.
Scala has a  very steep learning curve. Upto 3 months for a new dev.
Are there open source modules and libraries out there?
One of the neat things about scala is that java libraries can be used within scala,
and its built on top of JVM.

REST eg endpoint =
/api/organizations/{org_id}/?q=insights

How do you choose to nest a particular resource?
Are they friendly and easy to read?
--------------
2nd most important is that your endpoints have to be secure.
Since its plain text, malicious users can see it easily.
OAuth authentication cannot be done over HTTP. It has to be over HTTPS.
--------------
3rd requirement is leverage HTTP framework.
    a) make use of action verbs
CRUD ops =>  POST(create rsrc), GET (read-op), PUT(update), DELETE(del)
    b) standard headers
    c) return status codes - 200, 300, 400
--------------
4th requirement for good REST API design - Control levels of nesting
  Recommendation is api/1_level_of_collection?id/scope_apps
  eg =? api/org/id/jobs
  api/jobs/{job_id}

Get jobs at X -> returns a,b,c

Get details for a,b,c -> are these 3 calls or 1 call?
The endpoint here can be designed in batch mode here as
GET api/jobs/?q={a,b,c}

To support in just 1 call, we can do
/api/org/{org_id}/jobs?fields={id,name,location}
--------------
5th requirement = Pagination

Even if client hasn't asked for pagination, server has to have page-size defaults.

Serverless paradigm is very important for scalability.
Servers can fail but client-experience will be seamless.
Servers should persist state in persistent storage like distributed_file_system or shared cache
of K-V stores or DB. ie, externalize storage of result like -
 client_id|search_id|result_id

 and result_id|result_set

--------------
6th requirement = versioning of REST APIs
Without versioning, there cannot be backward compatibility.

By default, REST API comes with some amount of backward compatibility.

suppose in version 1, you were sending this response
result: {
    name:
    id:
}

in version 2, say you want to add count. Clients in v1 are not aware of count, but clients in v2
are aware of count.

Now clients will have to tell you what version they are using.
api/v2/org/blah

Should versioning be in http headers or in the api url itself?
----------------------------------------------------------------------
Design an amazon API for product reviews.

for a user to see a review,
GET amazon.com/products/{product_id}/reviews
------------
for a user to post a review,
POST amazon.com/products/{product_id}/review
to remove nesting we can have this POST request
request: {
    comment: "this is my comment"
    user: from session_id cookie
    timestamp: NOW()
}

response: {
    review_id:
}
status_codes_table
------------
for a user to update/edit a review or like a review
PUT amazon.com/products/{product_id}/reviews/review_id

since its too nested, how do you reduce nesting?
PUT amazon.com/reviews/review_id

POST amazon.com/reviews/review_id/like (is the `like` a PUT or a PUSH?)
We want to abstract it from the client, so POST is better.
------------

jobs: [
    {
        jobId: blah,
        external: True/False,
        contact:
    },
    ...
]
Based on external = True/False, client can take a different action.
"""







