"""
Introduction to http 504 Gateway timeout
A server (not necessarily a Web server) is acting as a gateway or proxy to fulfil the request by the
client to access the requested URL. This server did not receive a timely response from an upstream
server it accessed to deal with your HTTP request.

This usually means that the upstream server is down (no response to the gateway/proxy), rather than
that the upstream server and the gateway/proxy do not agree on the protocol for exchanging data.

Fixing 504 errors - general
This problem is entirely due to slow IP communication between back-end computers, possibly including
the Web server. Only the people who set up the network at the site which hosts the Web server can
fix this problem.

Use of proxies and caching is increasing on the Web. We do not have complete
control over where our HTTP request actually ends up. If only one link in the chain of computers
dealing with our HTTP request is broken, then an error such as 504 can easily occur.

Whenever you encounter 504 errors - there is nothing you can do to sort them out. We then have to
liaise with your ISP and the vendor of the Web server software so
that they can review the flow of IP data traffic between various computers under their control.
However this is not an easy error to sort out, because the ebb and flow of Internet traffic makes
this type of error very transient.

----------------------------------
504 errors in the HTTP cycle -
Any client (e.g. your Web browser) goes through the following cycle when it
communicates with the Web server:

1) Obtain an IP address from the IP name of the site (the site URL without the leading 'http://').
This lookup (conversion of IP name to IP address) is provided by domain name servers (DNSs).

2) Open an IP socket connection to that IP address.

3) Write an HTTP data stream through that socket.

4) Receive an HTTP data stream back from the Web server in response. This data stream contains
status codes whose values are determined by the HTTP protocol. Parse this data stream for status
codes and other useful information.

5) This error occurs in the final step above when the client receives an HTTP status code that it
recognises as '504'.
"""