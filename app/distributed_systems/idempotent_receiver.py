"""
https://martinfowler.com/articles/patterns-of-distributed-systems/idempotent-receiver.html
TODO - read all the distributed systems patterns in this series of blog posts

Idempotent receiver is a distributed systems pattern between request- response client-server architecture when
a client sends a request and either it doesnt reach the server or the server's response doesnt reach the receiver.

This was a question asked in Amazon interview by Erdinc Basci, Senior Principal Engineer.

In case of client failures after sending request and before receiving response, there can be 3 possibilities -
1) AT-MOST ONCE - client doesnt retry the request.
2) AT-LEAST ONCE - can cause duplicates.
3) EXACTLY ONCE - IMportant to have idempotent recievers in this scenario.

Some requests like adding a key-value pair is naturally idempotent. But creating a lease is not idempotent.
With idempotent receiver, the client will resend a request with the same request number, the server had generated a
response with that request number already, so it will just return that cached response. This would mean each client
generates its own request id. On the server side, state can be:

client_id | request_id | (serially_incrementing scheduling) event_id

The server response can be cached in the SESSION of the client request.

EXPIRING SESSIONS - If for the same client, the server had cached response for request_id X and it received
request_id Y where Y > X from the same client_id, then it can expire the  cached response for X and store the new
response for Y.

However, when there is REQUEST PIPELINING, ie multiple multiplexed requests in-flight on a single connection, you
will have to cache max in-flight requests in the client's session. eg - Kafka has a max of 5 in-flight requests/producer

A server can have max TTL for client sessions it stores. If there is no heart beat from the client during this TTL
window, client's state on the server can be removed. Server can have a scheduled task to periodically remove expired
sessions.



"""