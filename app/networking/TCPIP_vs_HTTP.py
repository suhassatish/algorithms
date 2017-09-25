"""
HTTP is a protocol used mostly for browsing the internet (IE, Firefox, etc).
It rides on top of TCP which provides a reliable link between two computers (if packet get lost -
it is re-transmitted). TCP itself rides on top of IP, which provides unified addressing to
communicate between computers. TCP/IP is a basis for internet and 99% of other networks.

TCP does a lot of interesting things to smooth over the rough spots of network-layer packet-switched
communication like reordering packets, retransmitting lost packets, etc. UDP is more unreliable, but
has less overhead. TCP is connection-oriented vs UDP is connectionless.

There are thousands of application-layer protocols:
    1) SMTP, IMAP, and POP3 for email;
    2) XMPP, IRC, ICQ for chat;
    3) Telnet, SSH, RDP for remote administration; etc.

TLS/SSL for instance provides encryption and session information between the network and transport
layers.
-------------------
TCP vs HTTP:

1)
HTTP is human readable which makes it easy to debug while binary TCP would mean writing a lot of
own tools, code generation, etc making things harder all around.

2) You are less likely to run into firewall issues if you use HTTP (default port 80) than if you use
TCP on some random port.

3) HTTP would make it easier to implement a load balancer between the external facing server and the
backend systems.

4) At the end of the day it is probably more important that your system is reliable, maintainable
and (maybe) scalable than it is fast. A sensible strategy is to implement the simple version first,
but have plans in your head for how to make it faster ... if the simple solution is too slow.

5) For a non-modern browser to directly consume TCP connections without HTTP you would have to use
Flash or Silverlight and this normally happens for rich content such as video and/or audio.

However, many modern browsers now (as of 2013) support APIs to access network, audio, and video
resources directly via JavaScript.
"""