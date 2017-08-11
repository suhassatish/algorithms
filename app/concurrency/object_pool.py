"""
An object pool is a pool of expensive objects like database connection objects.
Say DB can only handle 10 simultaneous connections.
We want to recycle these connections.
We want to have a limit of what we want to give out.
We want the functions get() which returns an object.
We want a free() which returns 1 of the objects back to the pool
get() will wait if limit reached.
At the beginning, pool is empty.
Bias towards giving out objects we have.

Hint: It'll make it easier if you use a conditional variable here.
"""
from threading import Lock
from collections import deque


class ObjPool(object):
    def __init__(self, limit):
        self.limit = limit
        self.count = 0
        self.mutex = Lock()

        self.full = Lock() # this is a condition variable
        # u want mutex to protect data structure unless some condition has occurred.
        # Producer says: I only want lock when its not full.
        # Consumer says: I only want lock when its not empty.
        # u only need as many cond_vars as there are number of booleans (is_full, is_empty)
        # condition variables have a phenomenon called spurious wake ups. The preferred way to use
        # it is within a while loop

        self.dq = deque()

    def get(self):
        """
        If anything in system memory heap, give it.
        Else create a new object and return it.
        :return:
        """
        # gives exclusive access
        self.mutex.acquire()

        while not self.dq and self.limit == self.count:
            self.full.acquire()

        if self.dq:
            o = self.dq.popleft()
        else:
            self.count += 1

        self.mutex.release()
        # lock should be as tight as possible

        # this is outside the mutex lock for performance reasons
        if o is None:
            o = Obj()
        return o

    def free(self, object):
        self.mutex.acquire()
        self.dq.append(object)
        self.full.release()
        self.mutex.release()


class Obj(object):
    pass
