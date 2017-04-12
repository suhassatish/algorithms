"""
Implement a concurrent hash-map using lock striping.
Note: Apply a locking strategy that offers better concurrency and scalability.
Instead of synchornizing every method on a common lock, restricting access to a single thread at a
time, utilize a fine-grained locking mechanism called lock striping to allow a greater degree of
shared access.
"""
# how many locks are required for k buckets?
# how do we handle the locks and provision them.
# contention to get locks
from threading import RLock


class ConcurrentHashMap(object):
    def __init__(self, capacity):
        self.size = 16
        self.d = dict(capacity)
        self.locks = [RLock()] * self.size

    def get(self, key):
        """
        returns value for key if it exists, else None
        Blocks if multiple readers
        """
        bucket_index = hash(key) % self.size
        self.locks[bucket_index].acquire()
        try:
            value = self.d[key]
        except KeyError:
            value = None
        self.locks[bucket_index].release()
        return value

    def put(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        bucket_index = hash(key) % self.size
        self.locks[bucket_index].acquire()
        try:
            old_value = self.d[key]
        except KeyError:
            old_value = None
        self.d[key] = value
        self.locks[bucket_index].release()
        return old_value
