"""
A thread pool is a group of pre-instantiated, idle threads which stand ready to be given work.
These are preferred over instantiating new threads for each task, when there is a large number of
short tasks to be done, rather than a small number of long ones. This prevents the overhead of
creating a thread a large number of times.

Implementation varies by environment, but the simplified requirements are:
1) A way to create threads and hold them in an idle state. This can be accomplished by having each
thread wait at a barrier (semaphore in ThreadPool2 implementation) until the pool hands it work.

2) A container to store the threads (this is missing in ThreadPool2 impl below but exists in
ThreadPool 1st impl below.

3) Also required is a standard interface or abstract class for threads to
use in doing work. This can be like the function f() in eg2 below that is passed into Thread()
constructor target variable which is executed by each individual thread created when t.start() is
called. In java, this might be an abstract class called Task with execute() method that does work.

4) When thread pool is created, it will instantiate a number of threads to make available or create
new ones as needed depending on the needs of the implementation.
When the pool is handed a task, it takes a thread from the Q (or waits for one to become available
if Q empty), hands it a Task, and meets the barrier. This causes the idle thread to resume execution
Once exe is complete, thread hands itself back to the pool to be put into the container for re-use
and then meets its barrier, putting itself to sleep until the cycle repeats.

TODO - trade offs of designs using thread pools
https://www.ibm.com/developerworks/library/j-jtp0730/

-------------------------------
count(threads) in thread pool

tasks.run() -> void

Support functions of add_work(Task f)

quit() -> finish work that thread pool has been given and then quit.

tp = ThreadPool(5)
tp.run()
tp.quit()

Any work started after quit has started, is undefined.

Hint: producer-consumer queue.
"""
import time
import logging
from Queue import Queue
from threading import Thread, Lock, currentThread, Semaphore
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)


class ThreadPool(object):
    def __init__(self, count):
        self.shutdown = None
        self.thread_q = Queue(maxsize=count)

    def quit(self):
        for i in xrange(self.thread_q.qsize()):
            self.add_work(self.shutdown)

    def add_work(self, task):
        self.thread_q.put(TaskThread())


class TaskThread(Thread):
    """
    This is required in java land, but is an overkill boiler plate code in python.
    A module function is sufficient.
    """
    def run(self):
        pass


class Scheduler(Thread):
    def __init__(self):
        Thread.__init__(self)
        q_size = 10
        tp = ThreadPool(q_size)
        for _ in xrange(q_size):
            tp.add_work(TaskThread())
        while tp.thread_q:
            task = tp.thread_q.get()
            task.run()

# Above is IK Yannis impl in class. Alternate thread pool implementation below.


class ThreadPool2(object):
    """
    This class tracks which threads are able to run at a given moment.
    A real resource pool would allocate a connection or some other value
    to the newly active thread, and reclaim the value when the thread is done.
    Here, it is just used to hold the names of the active threads to show that only
    10 are running concurrently.
    """
    def __init__(self):
        super(ThreadPool2, self).__init__()
        self.active = []
        self.lock = Lock()

    def make_active(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running: %s', self.active)

    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Running: %s', self.active)


def f(s, pool):
    logging.debug('Waiting to join the pool')
    with s:
        name = currentThread().getName()
        pool.make_active(name)
        time.sleep(0.5)
        pool.make_inactive(name)


if __name__ == '__main__':
    pool = ThreadPool2()
    s = Semaphore(3)
    for i in range(10):
        t = Thread(target=f, name='thread_'+str(i), args=(s, pool))
        t.start()
    # output:
    # (thread_0 ) Waiting to join the pool
    # (thread_0 ) Running: ['thread_0']
    # (thread_1 ) Waiting to join the pool
    # (thread_1 ) Running: ['thread_0', 'thread_1']
    # (thread_2 ) Waiting to join the pool
    # (thread_2 ) Running: ['thread_0', 'thread_1', 'thread_2']
    # (thread_3 ) Waiting to join the pool
    # (thread_4 ) Waiting to join the pool
    # (thread_5 ) Waiting to join the pool
    # (thread_6 ) Waiting to join the pool
    # (thread_7 ) Waiting to join the pool
    # (thread_8 ) Waiting to join the pool
    # (thread_0 ) Running: ['thread_1', 'thread_2']
    # (thread_3 ) Running: ['thread_1', 'thread_2', 'thread_3']
    # (thread_1 ) Running: ['thread_2', 'thread_3']
    # (thread_4 ) Running: ['thread_2', 'thread_3', 'thread_4']
    # (thread_2 ) Running: ['thread_3', 'thread_4']
    # (thread_5 ) Running: ['thread_3', 'thread_4', 'thread_5']
    # (thread_3 ) Running: ['thread_4', 'thread_5']
    # (thread_6 ) Running: ['thread_4', 'thread_5', 'thread_6']
    # (thread_4 ) Running: ['thread_5', 'thread_6']
    # (thread_7 ) Running: ['thread_5', 'thread_6', 'thread_7']
    # (thread_5 ) Running: ['thread_6', 'thread_7']
    # (thread_8 ) Running: ['thread_6', 'thread_7', 'thread_8']
    # (thread_6 ) Running: ['thread_7', 'thread_8']
    # (thread_7 ) Running: ['thread_8']
    # (thread_8 ) Running: []
