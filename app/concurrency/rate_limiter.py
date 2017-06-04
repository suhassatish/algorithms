"""
Design a rate limiter for concurrent API requests that can be used for throttling API requests from
any given API client based on configured quotas and security policy. Assume a basic rate limiting
policy like token bucket. In its simple form, one can also ask you to write code.
http://stackoverflow.com/questions/667508/whats-a-good-rate-limiting-algorithm

Makes sure system doesn't get over loaded
Limit to N requests/interval.
Interval = time in milliseconds.
Eg - 5 requests every 10s (numbers come from system performance analytics)


void onNewReq(Req r)
    process()

is (process)
    doWork(r)
else
    drop(r)

Keep a queue of N objects with timestamp.
If queue size reaches N, see the first element that came in and if

if now() - q[0].timestamp > interval:
    q.popleft()
    msgs_sent += 1


Take away: Does it make sense to make it multi-threaded? Maybe not.
Because reading from network card is very fast. Operations here are relatively quick.

If there is caching in the q, modify only in low volume situation. When 1st timestamp expired.

In high volume cases, like DDOS attack, this is when rate limiter is useful.

No point in putting multiple listeners on the same network card socket.

Never ever bring up unrelated concepts like lock-free data structures in an interview.

 -----------------------------
Another variant of asking this question is how to download a really large file through a web
browser, given infinite resource (cpu, memory, disk) in the cloud to design your backend (Quantcast)

EPI 21.10 distributed throttling casts this problem as a web crawler scraping websites, but
websites impose a limit that not more than b bytes can be downloaded from a website (by the crawler)
in a certain time period. Here you need to have a permissions-server which keeps track of how many
bytes have been downloaded from how many websites by a crawler in a given time-period.
If we are close to the quote, then the permission server may not allow the crawler to hit the
website. If we care about priorities and resource contention (since interviewer brought up Yarn
resource manager here, he was probably hinting at priority queue), permission-server may have a
queue to serve requests by various web crawlers. permission-server takes request from head of Q,
processes it (downloads file) and then notifies the web crawler when its download is completed.
If the permission server becomes the bottleneck, then we can scale it out horizontally.
The responsibility for a particular web_crawler_id may by hashed and go to a certain permission
server. Each permission server may be responsible for serving a few web crawlers and the crawlers
maybe crawling different websites such that no 2 crawlers scrape the same website.

Facebook had also reportedly asked this question on how to download a really large file?
There, the design expected may have been a peer-to-peer system like bit-torrent where parts of a
large file are stored on different hosts (peers).
Here, it downloads asynchronously and notifies when complete.
There is a design trade-off between fairness_index vs avg_download_time.
"""
from Queue import Queue
from datetime import datetime


def rate_limiter(message_received):
    """
    Queue solution maybe better than the below naive solution.
    A simple token-bucket algorithm without queue. If 5 messages have already been sent, in time
    interval, you drop the new message. Else, you lower the rate (throttle).
    :param message_received:
    :return:
    """
    rate = 5.0  # assume rate should be 5 messages every 8 seconds
    period = 8.0  # every 8 seconds
    allowance = rate
    last_check = datetime.now()

    while message_received:
        current = datetime.now()
        time_elapsed = current - last_check
        allowance += time_elapsed * rate/period
        if allowance > rate:
            allowance = rate  # throttle

        if allowance < 1.0:
            discard_msg(message_received)

        else:
            fwd_msg(message_received)
            allowance -= 1.0


def rate_limiter_2(request):
    q_size = 10
    q = Queue(maxsize=q_size)
    time_interval = 8.0  # every 8 seconds
    rate = 5.0

    def on_request_receive(req):
        current_time = datetime.now()

        if q.qsize() < q_size:
            # trivial case, we are not at the limit
            q.put((current_time, req))
            fwd_msg(req)
        else:
            sent = 0
            while current_time - q.peek() > time_interval and sent < rate:
                # the oldest request has expired, lets do work
                ts, rq = q.get()
                fwd_msg(rq)
                q.put((current_time, req))
                sent += 1
            else:
                # no space in queue which means all requests in the queue are still valid
                discard_msg(req)

    on_request_receive(request)


def discard_msg(request):
    pass


def fwd_msg(request):
    pass

