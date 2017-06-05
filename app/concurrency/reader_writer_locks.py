"""
Notes from concurrency class- Yannis:

Everything is built from semaphore.
Different type of lock leverages domain knowledge.
In a scenario of lots of reads, but not much writes/mutates, can we do something more efficient?
Yes, the answer is reader-writer lock. Can be built from other locks

Keeps track of readers.

in RWL impl, bias is towards readers. You dont want writers to completely starve. So real impl
will be more complex.

Up next: More granular control when data is changing. We dont want a huge critical section with
just 1 coarse-grained lock.

class RWL(object):
    def __init__(self, readers):
        self.lock = Lock()
        self.resource = Lock()
        self.readers = readers

    '''
    write_wait() {
        resource.wait()
    }

    write_signal() {
        resource.signal()
    }

    read_wait() {
        lock.wait()
        ++readers
        if readers == 1:
            resource.wait()
        lock.signal()

    read_signal() {
        lock.wait()
        --readers
        if readers ==0:
            readers.signal()

        lock.signal()
    }
    '''


class RWMap(object):
    '''
    A map that scales with reading.
    Goal is to get the most amt of scaling (concurrency)

    '''
    def __init__(self):
        self.lock = RWL(16)

        self.lock_with_bucket = []
        # namedtuple('Pair', ['rw_lock', 'bucket'])
        # this is an array of hash_maps
        # we need a tuple of bucket in hash-map associated with its RWL

    def put(self, key, value):
        '''
        This takes the writer lock. We dont have to ensure exclusive access to the whole map.
        Only a part that we're writing to, in the map can be locked.
        HashMap underlying impl is an array of buckets.
        Idea is to push down the lock to a fine grained lower-level of system. Adding complexity
        to get scalability. Problem is to make your own hash map
        :param key:
        :param value:
        :return:
        '''
        pass

    def get(self, key):
        '''
        Takes the read lock
        Returns value
        :param key:
        :return:
        '''
        hash_code = hash(key)
        self.lock.read_wait()
        index = hash_code % len(self.lock_with_bucket)
        self.lock_with_bucket[index][0].read_wait()
        '''
        map = pair[key].(l)
        val v = m[key]
        pair[key][0].read_signal()
        lock.read_signal()
        return v
        '''
        pass

2yannis@gmail.com
------------------------------------------------------------
"""
import threading

__author__ = "Mateusz Kobos"


class RWLock(object):
    """Synchronization object used in a solution of so-called second
    readers-writers problem. In this problem, many readers can simultaneously
    access a share, and a writer has an exclusive access to this share.
    Additionally, the following constraints should be met:
    1) no reader should be kept waiting if the share is currently opened for
        reading unless a writer is also waiting for the share,
    2) no writer should be kept waiting for the share longer than absolutely
        necessary.

    The implementation is based on [1, secs. 4.2.2, 4.2.6, 4.2.7]
    with a modification -- adding an additional lock (C{self.try_rd})
    -- in accordance with [2].

    Sources:
    [1] A.B. Downey: "The little book of semaphores", Version 2.1.5, 2008
    [2] P.J. Courtois, F. Heymans, D.L. Parnas:
        "Concurrent Control with 'Readers' and 'Writers'",
        Communications of the ACM, 1971 (via [3])
    [3] http://en.wikipedia.org/wiki/Readers-writers_problem
    """

    def __init__(self):
        self.rd_switch = _LightSwitch()
        self.wr_switch = _LightSwitch()
        self.rd_lock = threading.Lock()
        self.wr_lock = threading.Lock()
        self.try_rd = threading.Lock()
        """A lock giving an even higher priority to the writer in certain
        cases (see [2] for a discussion)"""

    def reader_acquire(self):
        self.try_rd.acquire()  # Indicates a reader is trying to enter
        self.rd_lock.acquire()  # lock entry section to avoid race condition with other readers
        self.rd_switch.acquire(self.wr_lock)  # lock writers out.

        self.rd_lock.release()  # release entry section for other readers
        self.try_rd.release()  # Indicates you are done trying to access the resource

    def reader_release(self):
        self.rd_switch.release(self.wr_lock) # But as soon as 1 reader is done, a
        # new writer has a chance to acquire the wr_lock

    def writer_acquire(self):
        self.wr_switch.acquire(self.try_rd)  # 1st writer locks readers out
        self.wr_lock.acquire()  # reserve entry section for writers - avoids race conditions

    def writer_release(self):
        self.wr_lock.release()  # release exit section
        self.wr_switch.release(self.try_rd)  # last writer releases read_try lock for readers;
        # this may cause reader starvation. Solution - 3rd readers-writers problem


class _LightSwitch(object):
    """An auxiliary "light switch"-like object. The first thread turns on the
    "switch", the last one turns it off (see [1, sec. 4.2.2] for details)."""

    def __init__(self):
        self._counter = 0
        self._mutex = threading.Lock()

    def acquire(self, lock):
        self._mutex.acquire()
        self._counter += 1
        if self._counter == 1:
            lock.acquire()
        self._mutex.release()

    def release(self, lock):
        self._mutex.acquire()
        self._counter -= 1
        if self._counter == 0:
            lock.release()
        self._mutex.release()
