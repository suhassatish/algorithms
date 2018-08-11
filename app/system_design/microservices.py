"""
StitchFix Talk on Microservices at Global Big Data SW Architecture Conference, Jun 2017
@randyshoup
Shared on slide share already.

For companies to be successful with microservices, it has to have a strong CI/CD engg culture,
devOps mind-set.

Ruby on rails applications, deployed multiple times a day. Continuous delivery to release smaler
units of work. Easier to roll back and roll forward. Small experiments and rapid iterations.

DevOps - same team that builds a thing, runs the thing in production. End-to-end ownership.
Team owns service from design to deployment to retirement. Same ppl responsible for features,
quality, perf, ops, maintenance.
-----------
eBay evolution to microservices - 5th gen today
monolithic perl -> monolithic C++ -> java -> polyglot microservices
16k = compiler limits on compilation.

Similar evolutions at Twitter, Amazon.
Notice: No one started with microservices, everyone started as a monloithic web app, but moved to
microservices with scale.
-----------
First law of distributed object design - Dont distribute your objects.
If you dont end up regretting your early technology choices, you probably over-engineered.
-----------
What are microservices? Microservices are nothing more than SOA done properly.

1) micro part is the scope of the interface. Single line of responsibility.
2) single-purpose
3) modular and independent
4) Isolated persistence! - Individual microservices own their own backend data stores.
No back doors to violate your interface. 4) is where eBay went wrong. In 2008, they created awesome
beautifully designed services but DB was shared. Everyone started back dooring.

Could be a separate schema for each microservice.
-----------
Approach1 - Operate your own data store. Use postgres at StitchFix

Approach2 - Use a persistence service- like RDS, DynamoDB, spanner, azure Storage.
Isolated from all other users of the service.

Only external access to data store is through published interface.
----------------------------------------------------------------------------------------
Events as first-class construct in our architectural tool box -

1) Whats an event? A significant change in state. eg - Item added to shopping cart, box sent.
0 or 1 or N consumers subscribe to the event, typically asynchronous.

Event is the Fourth fundamental building block -
1) Presentation -> interface/interaction
2) Application -> stateless biz logic
3) Persistence -> DB
4) State changes -> events. Example - async bank transactions for buy/sell stocks fired at each
other thru-out the day. Differences reconciled at the end of the day.

----------------------------------------------------------------------------------------
A service interface includes -

1) gRPC, REST - interface specification
2) events that consume from the service
3) events that produce into the service
----------------------------------------------------------------------------------------
Where does shared data go in a microservices world?

Principle: Single system of record. 1 WR and many Read-only, non-authoritative shared copy.

Customer service sends an event to order service whenever a new customer event happens.
The order service caches that data.

In stitch-fix,
item-service

style-service

receiving-service

eg - US states, colors, sizes, etc
----------------------------------------------------------------------------------------
Joins are super-easy in monolithic world but are a challenge in microservice world.
Several approaches to this -

1) Join in client application: order-history-page - all orders for a customer

2) Slightly more complicated approach - materialized views. Listen to events from item-service
and order-service. Maintain denormalized join of items and orders together in local storage.

Its great for many-many relationships that are difficult to join in real-time.
Every noSQL does this. RDBMS optimizes for write, reads need expensive joins.

Cassandra, Riak optimizes for read by writing in parallel very quickly.

"""