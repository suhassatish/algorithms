"""
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
        #heapq.heappush(pq, curr_time)
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
        #for e in self.pq:
        #    copy_pq.append(e)
        count = 0
        for key, val in self.st.iteritems():
        #while curr_time - copy_pq[0] < 300:  # unit in seconds
            if curr_time - key < 300:
                count += val
            #heapq.heappop(copy_pq)
        return count
