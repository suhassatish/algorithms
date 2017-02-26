"""
Design a least-recently-used cache, which evicts the least recently used item.
Lets come up with the API methods first for the cache.

Design talking points:
Redis and memcached are popular open source caches. memcached is more low-level and
stores only byte arrays. But redis can also store higher-level denormalized objects,
making it more human-readable.

Redis has different eviction schemes like FIFO, round robin, LRU, etc.

Then go into discussion about API methods, time complexity requirements of each depending on
access patterns and come up with data structures to achieve those SLAs. Look at docstring of
 individual methods below for talking points.

Then finally talk about open-ended brain storming discussions like what happens if latency is a lot.
How to reduce it? Talk about distributing or partitioning key space.
Can also discuss about lock-free data structures if you know about concurrency at scale.

https://discuss.leetcode.com/topic/24757/python-concise-solution-with-comments-using-ordereddict/2
"""
from collections import deque, OrderedDict


class LRUCache(object):

    def __init__(self, capacity_int):
        self.capacity = capacity_int
        self._map = {}  # this is an internal hash map of {Key k : DLLNode<K,V> value}

        # this data structure is to achieve the evict() operation in O(1) time
        self._dll = deque(maxlen=capacity_int)

    def get(self, key):
        """
        Here you have to ask and clarify from the interviewer if you need to return
        only the most recent version of the value or multiple versions (example different
        timestamped versions of a file in dropbox)

        By using a priority queue, get can be achieved in O(lg n) time
        :param key:
        :return: list of all values for key. If key doesnt exist, returns -1
        """
        if key not in self._map:
            return -1
        self._dll.remove(key)
        self._dll.append(key)
        return self._map.get(key)

    def put(self, key, value):
        """
        If key already exists, it over-writes the value with new value
        If key doesn't exist, it adds new key, value pair into the cache

        Design talking points:
        By using a priority queue, put can be achieved in O(lg n) time
        By using hashmap, we can do better with O(1) amortized time, except when doubling size
        if capacity is reached.

        When you try to insert into a full cache, it has to trigger evict.
        We can either block on evict, or could handle it asynchronously.
        Here, we are going to assume single line of responsibility for each method to have low
        coupling and high cohesion between different OO methods.
        :param key:
        :param value:
        :return: None
        """
        if key in self._map:
            self._dll.remove(key)

        elif len(self._map) == self.capacity:
            evicted_key = self._dll.popleft()  # remove lease recently used element
            self._map.pop(evicted_key)

        self._dll.append(key)
        self._map[key] = value

    def remove(self, key):
        """
        The signature here will depend on if K:V is 1:1 or 1:many
        For 1:1, input takes only key. For 1:many, signature is remove(key, value)
        :param key:
        :return:
        """
        pass

    def _evict(self):
        """
         This is an internal method.
         It can be implemented efficiently with a doubly-linked list (DLL) with head & tail pointers
         The value V always points to the element in the DLL. Every time an element is accessed,
         move the element in DLL from head to tail.
         Tail always has the newest and head the oldest
         This gives us O(1) operation for eviction.
        :return:
        """
        pass
