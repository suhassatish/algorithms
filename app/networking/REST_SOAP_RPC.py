# -*- coding: utf-8 -*-
"""
https://apihandyman.io/do-you-really-know-why-you-prefer-rest-over-rpc/
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
----------------------------------
REST vs SOAP (Simple Object Access Protocol)

1) SOAP is a protocol vs REST is an architectural style (REST can work with HTTP or any other
protocol too. As long as there's a starting URI entry point to connect to. Resources
are spposed to return links in server response the clients should follow.)

2) SOAP client works like a desktop application, tightly coupled to the server.
    There's a rigid contract that can break with a change on either side.

3) REST is not a mapping between HTTP methods to CRUD operations.

4) Security - SOAP's WS-Security is more robust than REST which has to rely on the underlying protocol, ie
in the most common case, HTTP. SSL is point-to-point and is supported by both REST & SOAP.
Reference: https://stackify.com/soap-vs-rest/

5) Retry logic - SOAP has built-in retry logic if communication fails, but in REST, client has to retry.

6) SOAP's standard HTTP protocol makes it easier to operate across firewalls and proxies without modifications
to the SOAP protocol iteself. But it uses the complex XML format (vs REST which allows greater variety of data
formats)  making it slower compared to middleware such as ICE and COBRA.

7) For greater ACID transactional reliability, SOAP is the way to go.

8) SOAP is highly extensible through other protocols and technologies. In addition to WS-Security, SOAP supports WS-Addressing, WS-Coordination, WS-ReliableMessaging, and a host of other web services standards, a full list of which you can find on W3C.

9) Most new APIs are built using REST and JSON, simply because it typically consumes less bandwidth and is easier to understand both for developers implementing initial APIs as well as other developers who may write other services against it.

10) REST provides superior performance, particularly through caching for information that’s not altered and not dynamic.

11) REST uses WADL vs SOAP uses WSDL (see below)
------------------------
WSDL stands for Web Services Description Language
WSDL is used to describe web services
WSDL is written in XML.
WSDL is used by SOAP.
https://www.w3schools.com/xml/xml_wsdl.asp  - WSDL syntax format with examples

JAXB (java architecture for XML binding) is a JAVA API for parsing and generating XML. This can be used in addition to
the DOM (document object model).
-------
WADL - Web Application Description Language - This is a machine-readable XML description of HTTP-based web services.
WADL is the REST equivalent of SOAP's Web Services Description Language (WSDL), which can also be used to describe REST
web services.

Jersey is the java library reference implementation to generate java code from an existing WADL. Apache CXF is another
library that does it.
-----------------------------------------------------------
WSDL vs WADL

WSDL is the Web Services Description Language. It is commonly used to spell out in detail the services offered by a SOAP
 server.

While WSDL is flexible in service binding options (for example, services can be offered via SMTP mail servers),
 it did not originally support HTTP operations other than GET and POST.

Since REST services often use other HTTP verbs, such as PUT and DELETE, WSDL was a poor choice for documenting REST
 services.

WADL is the Web Application Description Language. WADL is championed by Sun Microsystems. Like the rest of REST, WADL
is lightweight, easier to understand and easier to write than WSDL. In some respects, it is not as flexible as WSDL
(no binding to SMTP servers), but it is sufficient for any REST service and much less verbose.

"""