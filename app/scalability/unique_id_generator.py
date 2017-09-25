"""
Design a random/unique ID generator (on a distribution of servers) or ticket server.

Use cases: Any place that gets millions of requests generally gets an ID, eg logs or analytics, etc
Discuss how DBs can generate auto-incrementing unique IDs. When generating from multiple machines, attach TimeStamp (TS)
to each UID from each m/c and also machine_id.

All servers need to be on a single timezone. NTP is a standard way to do this.

Requirement: low disk latency, lwo network latency.

References -
https://segment.com/blog/a-brief-history-of-the-uuid/
https://stackoverflow.com/questions/2671858/distributed-sequence-number-generation
https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake.html
https://www.slideshare.net/davegardnerisme/unique-id-generation-in-distributed-systems

"""