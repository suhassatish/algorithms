"""
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
from collections import deque
from threading import Thread, Lock, currentThread, Semaphore
dq = deque()
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)


class ThreadPool(object):
    def __init__(self, count):
        self.count = count
        self.shutdown = None
        threads = []
        for i in xrange(count):
            threads[i] = TaskThread(count)

    def quit(self):
        for i in xrange(self.count):
            self.add_work(self.shutdown)

    def add_work(self, task):
        dq.append(task)


class TaskThread(Thread):

    def run(self):
        while True:
            task = dq.pop()
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
