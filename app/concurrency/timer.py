"""
Design a "timer" scheduler that can take a number of specified tasks and schedule them for
execution after specified time-interval delay. What would be some of the design considerations to
ensure efficiency, resiliency and support for monitoring progress?

It is very easy to imagine a complex scheduling system when solving this problem (think cron +
stopWatch + timer). But keep it limited in scope.

Asked in Twitter onsite interview in Dec 2014.
----------
EPI Pg 354 20.8
There are 2 aspects to this problem - data structure design and concurrency.
We can have a timer class that takes 2 arguments to its constructor - an object that has a run()
method and a string with the name for the thread.

1) We can have a priority queue (min-heap) of execution_time as the key and the value = thread to run.
PQ entries -
[(timestamp_1, thread_id1), (timestamp_2, thread_id2), ...]

2) We will need a 2nd DS hashMap of thread_id to the entry in the minPQ.
{
    thread_id1: timestamp_1,
    thread_id2: timestamp_2,
    ...
}
3) A dispatcher will periodically wake-up and take time_diff of now() - pq[0].peek() and if its
close to 0, it will pq.del_min() and then execute the task with thread_id, in a new thread.
    a) Dispatcher is woken up if a new thread is added to the hashMap or removed from it.
    b) If woken up, it recomputes its remaining sleep time based on (pq.peek() - now())
    c) If a scheduled time has arrived, the dispatcher does pq.del_min() and executes the job
    d) If insertion is at the top of min-heap, we interrupt the dispatch thread so it can alter its
    wake-up time.

4) If a scheduled job is cancelled, it is removed from the hashMap and deleted from the PQ.
Cancel request can be ignored if the thread has already started.
Probably need an IndexMinPQ here with API for change_key(), increase_key(), decrease_key(),
delete(), insert(), del_min(). You can delete or change_key by the index.
Also should support peek() at the min-key.
Also supports contains(), size(), key_of(index) returns key,
"""

# Timers call a function after a specified number of seconds:
from threading import Thread
import time
from threading import Event


class Timer(Thread):
    """
    The dispatcher thread described from EPI above will be implemented like this Timer.
    Implementation copied from std lib threading.Timer
    Call a function after a specified number of seconds:

            t = Timer(30.0, f, args=[], kwargs={})
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting

    """

    def __init__(self, interval, function, args=[], kwargs={}):
        Thread.__init__(self)
        # this is in the threading lib specification when Thread class is sub-classed
        # If a subclass overrides the constructor, it must make sure to invoke
        # the base class constructor (Thread.__init__()) before doing anything
        # else to the thread.

        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()  # default = False
        # An event manages a
        # flag that can be set to true with the set() method and reset to false
        # with the clear() method. The wait() method blocks until the flag is true.

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()  # sets finished = True

    def run(self):
        self.finished.wait(self.interval)
        # blocks as long as finished = False, or until timeout, ie interval
        # if finished = True, returns immediately.

        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()


def f():
    pass


def foo():
    """
    This is a method which runs periodically calling itself every 10 seconds, and a new thread
    is run asynchronously in the background, without blocking. Great application of Timer to execute
    periodic actions in python.
    :return:
    """
    print(time.ctime())
    Timer(10, foo).start()


def set(self):
        """
        This is an under-the-hood implementation of Event().set() below.
        Uses condition variable.
        Set the internal flag to true.

        All threads waiting for the flag to become true are awakened. Threads
        that call wait() once the flag is true will not block at all.

        """
        self.__cond.acquire()  # threading.Condition
        try:
            self.__flag = True  # initialized to False in constructor
            self.__cond.notify_all()
        finally:
            self.__cond.release()


if __name__ == '__main__':
    t = Timer(30.0, f, args=[], kwargs={})
    t.start()  # calls Thread.start() and must be called at-most once per thread object.
    # It arranges for the object's run() method to be invoked in a separate thread of control.
    # start() will raise RuntimeError if called more than once on same thread object.

    t.cancel()  # stop the timer's action if it's still waiting
