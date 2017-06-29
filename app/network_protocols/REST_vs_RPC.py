"""
TODO - https://apihandyman.io/do-you-really-know-why-you-prefer-rest-over-rpc/
REST vs thrift differences? Asked by Tom Gianos at Netflix onsite.
REST is a general architectural style for APIs leveraging HTTP and related Web technologies with
the endpoints being resources (like DB tables). You call HTTP verbs on these resources to perform
CRUD operations. GET (read), PUT (update), POST (create), DELETE (delete).

While Thrift/gRPC are specific RPC systems where your "END POINTS ARE ACTIONS", instead of resources
RPC is agnostic to the transport mechanism used to implement your API, and can be implemented using
a) HTTP, b) message queues, or c) files.

1) Both RPC and REST use HTTP protocol (most commonly) which is a request/response protocol.
2) Thrift and Avro come with RPC support included.

When should you use REST?
    If interoperability is your primary concern, nothing beats REST. There are no special
    technologies needed, and you can leverage all of the widely deployed infrastructure and tools
    that support the modern Web.

When should you use RPC?
    1) If performance is your primary concern, RPC can provide an edge by leveraging serialized data
    formats (binary) and alternative transport mechanisms (eg - thrift over TCP instead of HTTP).

    2) With RPC, you can avoid parsing JSON responses or extracting query path parameters. RPC is
    also transport agnostic, and you may be able to leverage different behaviour by using an
    alternative transport mechanism like a message queue.

"""