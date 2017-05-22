"""
http://www.madhur.co.in/blog/2015/11/02/countdownlatch-python.html
How to implement a count down latch in python, similar to java constructs
Count down latch is a synchronization technique that allows a thread to wait until work in other
threads completes.

eg application - You may have an asynchronous API call, and you may want to do
it in a multi-threaded API call, and then take some action when all of them complete, or another
action even if one of them fails.
------------------------------------------------------------------------------------------------
In java, latch.await() is a blocking call that waits until both async msg calls to API either
succeed or 1 of them fails. Its better than spin-lock or busy-waiting.

CONS OF USING SPIN-LOCKS -
1) Spin-lock or spinning is considered an anti-pattern and should be avoided, as processor time that
could be used to execute a different task, is instead wasted on useless activity sending a NOP
through the CPU pipeline.

2) Spinlocks become wasteful if held for longer durations, as they may prevent other threads from
running and require rescheduling.

3) The longer a thread holds a lock, the greater is the risk that the thread will be
interrupted by the OS scheduler while holding the lock. If this happens, other threads will be
"spinning" (trying to acquire the lock) while the thread that has the lock is not making progress
towards releasing it.

PROS OF USING SPIN-LOCKS -
1) Spinlocks are efficient if threads are likely to be blocked for only short periods.
For this reason, operating-system kernels often use spinlocks.
------------------------------------------------------------------------------------------------

"""
import threading
import random

RETRIES_COUNT = 4


def send_notification_task(**kwargs):
    """
    This is an example dummy application to illustrate the usage of CountDownLatch()
    :param kwargs:
    :return:
    """
    latch = CountDownLatch(1)
    status = {'result': 0}
    user_id = 16182

    msg = (user_id, 'This is a sample msg')

    def _callback(message):
        status['result'] = 1
        latch.count_down()

    def _error(message):
        status['result'] = 2
        latch.count_down()

    publish(msg, _callback, _error)
    latch.await()

    if status['result'] == 1:
        return 'success'

    elif status['result'] == 2:
        countdown = int(random.uniform(2, 4) ** RETRIES_COUNT)
        retry(countdown=countdown)


class CountDownLatch(object):

    def __init__(self, count):
        """
        This uses a condition() from the python threading library, which is a factory function that
        returns a condition variable object. Condition variables allow one or more threads to wait
        until they are notified by another thread.
        :param count:
        :return:
        """
        self.count = count
        self.lock = threading.Condition()

    def count_down(self):
        self.lock.acquire()
        self.count -= 1
        if self.count <= 0:

            # if the calling thread has not acquired the lock when this method is called, a
            # RuntimeError is raised
            self.lock.notify_all()
        self.lock.release()

    def await(self):
        self.lock.acquire()

        # condition variables have a phenomenon called spurious wake ups. To prevent that, the
        # preferred way of calling it is within a while loop.
        while self.count > 0:

            # wait until notified, or a timeout occurs.
            # if the calling thread has not acquired the lock when this method is called, a
            # RuntimeError is raised
            self.lock.wait()

        self.lock.release()


def retry(countdown):
    """
    Dummy method that retries to send a msg. Client applications need to call this with exponential
    back-off upon failure
    :param countdown:
    :return:
    """
    pass


def publish(s, callback_fn, error_fn):
    """
    This is a dummy mock of Java pubnub library for illustration
    :param s:
    :param callback_fn:
    :param error_fn:
    :return:
    """
    pass
