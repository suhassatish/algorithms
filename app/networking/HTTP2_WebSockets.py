"""
HTTP/2 is a new version of HTTP that uses a single, multiplexed connection to allow multiple requests to be sent on
the same connection. It also compresses header data before sending it out in binary format and supports
SSL connections to clients.

WebSockets allows a server to exchange real-time messages with end-users without the end users having to request
(or poll) the server for an update. WebSockets protocol provides bi-directional communication channels between a client
and a server over a long-running TCP connection. This is the defactor communication protocol for chat applications.

Server-sent events (SSE) is a server push technology alternative to web sockets via a HTTP connection, standardized as
part of HTML5. This is more suitable for publish subscribe scenario like streaming stock prices, twitter feeds update
and browser notifications.

"""