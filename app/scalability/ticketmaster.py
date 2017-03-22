"""
Ticket booking service.

Theatres/Movies -> Showtinmes -> Auditorium -> Seat Selection -> Purchases
theatres table
|theater_id|auditorium_id|capacity|location|

movies
|movie_id|theatre_id|auditorium_id|showtime_id|movie_length|

showtimes

In seat selection phase, there's an interesting transaction happening here.
Service shows a 5-minute time-to-expiry.
Lets talk about the microservice doing this.

Payment service should co-ordinate with seat-selection service.

Is the seat-selection a kafka event or a database event?

have a seat_transactions database.
seat transaction is a seat_id locked by user_id, hold it for lock_created_at_timestamp
hold the lock and publish to kafka, then payment gateway finalizes commit transaction.

status now changes from blocked -> booked in seat-Tx-DB;
There are 2 services acting on the same collection.

Is it a good pattern or a bad pattern?
Its a bad pattern because each microservice should be isolated from each other.
If payment service corrupts one of the fields, it causes repurcussions everywhere.
Violates single-line-of-responsibility.

Use messaging system to highlight & decouple the propagation of state between services.
Maintaining DB isolation is an important pattern in SOA.
--------------
If you think of a start-up evolution,
BizLogic is a monolith with an API. Most start-ups start that way.


Thrift RPC is light-weight, allows interoperability across different languages.
DBaaS = BigTable, Spanner at Google

At what level do microservices share database tables? Can they share tables or rows or database
isolation is required or separate clusters?

Scatter-gather pattern. eg - Spark driver to executors.


What are the trade-offs of REST vs Thrift?
REST = http = layer7 => opening 2 more layers in OSI stack. (presentation, session)
thrift = TCP = faster

Docker gives tools like compose which can help you easily manage services and isolation.
Running on same-server vs different looks the same with docker. SOA is a green field.
"""