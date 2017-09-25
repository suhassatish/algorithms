"""
Asked by Todd Lipcon in Cloudera interview.
End to end encryption achieved using public - private key encryption.
Its not decrypted by the web servers.

Messaging using Kafka. Topics with partitions. Hash partitioning with consistent hash ring.

Some more questions to think about -
How many users are we talking about here?
How many messages sent?
How many messages read?
What are the latency requirements for sender->receiver message delivery?
How are you going to store messages?
What operations does this data store need to support?
What operations is it optimized for?
How do you push new messages to clients? Do you push at all, or rely on a pull based model?
------------------------------------------------------------------------------------------------
How to achieve exactly-once messaging semantics?

MemSQL pipelines (kafka consumer) combined with Kafka can achieve exactly once semantics.
Achieved by co-locating kafka consumer offsets along with data.
MemSQL stores the kafka offset in a table.

An alternative approach is to use atleast-once semantics
to simulate exactly-once semantics by ensuring idempotency or otherwise eliminating side effects
from operations. State changes are idempotent and applying the same state change multiple times
does not lead to inconsistencies as long as the application order is consistent with the delivery
order.
------------------------------------------------------------------------------------------------
http://highscalability.com/blog/2014/2/26/the-whatsapp-architecture-facebook-bought-for-19-billion.html

1)
Multimedia messages are sent by uploading audio, video or image to a HTTP server and then
sending a link to the content along with its base-64 encoded thumbnail.

2)
Each user is represented by an actor model in Erlang. Alice the actor can retry sending
messages to Bob the actor with exponential back-off until its acknowledged.
If the server ecosystem supports non-blocking IO, it can open upwards of 10k connnections
on a single box. JVM has netty library, python has twisted and tornado.

3)
WhatsApp uses XMPP protocol.
XMPP is mostly like HTTP where the client opens the socket with the XMPP server and keeps it open
as long as the client is logged in. It's not like the regular REST API where the client opens the
socket send/receive the data and close the socket. The socket is opened as long as you are signed
in.

4) A primary gauge of system health is message queue length. The message queue length of all the
processes on a node is constantly monitored and an alert is sent out if they accumulate backlog
beyond a preset threshold.

When message queue backlogs became large garbage collection would destabilize the system.
So pause GC until the queues shrunk.
------------------------------------------------------------------------------------------------
https://www.facebook.com/notes/facebook-engineering/building-facebook-messenger/10150259350998920/
Building Facebook Messenger (Chat) - 2011

1) Use MQTT protocol to maintain persistent connection from mobile device to backend server without killing battery life
This is to solve the problem of reliable but slow msg send. MQTT specifically designed to send telemetry data from and
to space probes. Uses B/W sparingly. Result: phone-phone delivery in 100s of ms.

"""