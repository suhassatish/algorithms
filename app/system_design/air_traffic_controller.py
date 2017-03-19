"""
Air Traffic Controller (ATC) Requirements:
1) Safety of departures, landing
2) # of run ways
3) Gates
4) Itinerary = how its supposed to fly (has schedule/time)
5) Path = how it really flew
6) weather conditions (fog, visibility)
7) ground conditions - flood, ice/snow, etc

Aircraft like Boeing 747 is a physical object.
Flight like MH 370 is an abstraction tied to an itinerary.

ATC is a mediator pattern. Use when lots of objects trying to co-ordinate among themselves,
and there's difficulty in managing that communication.

Mode of communication - how to model?
Ack-based system
Observer/observable - wait/notify/signal;
msg passing; asynchronous; MessageHandler; IMPORTANT: These 3 are the most important in any msging
communication model;

Radio channel communication - not easy to do point-to-point; it has to be broadcasted;
msg has a payload; what kind of messages maybe in the payload?

class Message(object):
    payload
    type (some bytes will tell you the type request/response then route it to correct ATC controller
        or flight)

Aircraft     ATC
    message ->
            process()
    <- ack

Internally, ATC has to maintain priority queues.
There will be multiple controllers in ATC. Scan the msg to determine which grid it needs to go to.

Consumer (aircraft) pulls from the queue.

There are different types of messages - trying to backup from parking gate,
trying to taxi after landing, trying to take-off, trying to land, etc

How to model this if-else condition depending on communication from queues?

MessageHandler <-> consumer <-> msgType <-> queue


DataPoint -> DataProvider -> ATC -> Update_State
                                       |  poll()
                                       V
                                     Handler (polls state)

Define an interface, do handlers and delegate them. That's a far cleaner design than to have a
nested if-else of deep-nesting.


Degradation of code happens when there are change of requirements.
First production symptoms = Unintentionally someone else broke your business flow.
These things you will realize only when you refactor.

"""