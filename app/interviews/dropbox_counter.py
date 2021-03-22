"""
This question is often asked in Dropbox phone interviews.
Its also called request counter or hit counter system design.
Count # of visitors in past 1 minute [or 5 minutes, hour, or all of the above]

Important points -
1) Circular buffer is central to design
2) Concurrency is important. For low volumes, locking is ok. FOr higher volume, asynchrounous writes are a must.

https://stackoverflow.com/questions/17562089/how-to-count-number-of-requests-in-last-second-minute-and-hour
https://stackoverflow.com/questions/18396452/design-a-datastructure-to-return-the-number-of-connections-to-a-web-server-in-la
http://prismoskills.appspot.com/lessons/System_Design_and_Big_Data/Chapter_03_-_Count_requests_in_last_second_and_hour.jsp
----------------------------------------------------------------------------------------------------
Distributed counter -
Use case - 100 billionth visitor on Google gets a raffle prize.

1) Canonical answer - http://www.cakesolutions.net/teamblogs/how-to-build-a-distributed-counter

2)  http://highscalability.com/blog/2009/2/18/numbers-everyone-should-know.html
Reasonably acceptable answer. A bit hand-wavy but conveys sufficient knowledge.

3) lazy answer - use a distr K-V store to do this
http://blog.memsql.com/high-speed-counters/

4) However in practical systems, this will be mixed with existing data pipelines.
How facebook does it with Hbase -
http://highscalability.com/blog/2011/3/22/facebooks-new-realtime-analytics-system-hbase-to-process-20.html

How twitter does it -
https://www.slideshare.net/kevinweil/rainbird-realtime-analytics-at-twitter-strata-2011/40-Multiple_Formulas_So_far_we

Research paper -Scalable Eventually Consistent Counters over Unreliable Networks
https://arxiv.org/pdf/1307.3207v1.pdf

----------------------------------------------------------------------------------------------------
this gets called every time my site gets a hit
log_hit()
will be called once in a while
returns number of hits in the last 5 minutes.
get_hits() -> int
not strict on accuracy of timestamp
"""
import time


class WebHits(object):
    """
    Optimal data structure - circular double ended queue which can add and remove elements
    from both ends in O(1) time. You always add to head, you always remove expired entries from tail
    For randomized access to any element in deque, the underlying implementation should be an array
    of arrays with each sub-array being a fixed size, say 10. And totally there should be 30
    elements in outer array. So 30 * 10 = 300 = 5 minutes.
    """
    def __init__(self):
        # self.pq = []
        self.st = {}

    def log_hit(self):

        curr_time = int(time.time())
        # heapq.heappush(pq, curr_time)
        if curr_time not in self.st:
            self.st[curr_time] = 1
        else:
            value = self.st[curr_time]
            value += 1
            self.st[curr_time] = value

        for e in self.st:
            if curr_time - e > 300:
                self.st.remove(e)
                # heapq.heapremove(self.pq, e)

    def get_hits(self):
        """
        Gets hits only in the last 5 minutes
        """
        curr_time = int(time.time())
        # copy_pq = list()
        # for e in self.pq:
        #    copy_pq.append(e)
        count = 0
        for key, val in self.st.iteritems():
            # while curr_time - copy_pq[0] < 300:  # unit in seconds
            if curr_time - key < 300:
                count += val
            # heapq.heappop(copy_pq)
        return count
