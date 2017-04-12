"""
A hash set that can take no more than N items in the set.
If it has N items, it blocks when full.

"""
from threading import Lock, Semaphore


class BoundedHashSet(object):

    def __init__(self, capacity):
        """
        Lock is a mutex or a semaphore with count = 1
        This is used to guard the critical section and ensure mutual exclusion so only 1 thread
        has access at a time.

        Semaphore is to enforce capacity. Everytime sem.acquire() is called, capacity decrements
        by 1. When sem.release() is called, capacity increments by 1. If sem.acquire() is called
        when capacity  == 0, it blocks.
        :param capacity:
        :return:
        """
        self.mutex = Lock()
        self.st = set()
        self.sem = Semaphore(capacity)

    def add(self, item):
        if item not in self.st:
            self.sem.acquire()

        self.mutex.acquire()
        self.st.add(item)
        self.mutex.release()

    def erase(self, item):
        self.mutex.acquire()
        self.st.remove(item)
        self.mutex.release()
        self.sem.release()
