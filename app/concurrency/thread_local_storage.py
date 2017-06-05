import threading
import logging
import random

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-0s) %(message)s',)


def show(data):
    try:
        val = data.val
    except AttributeError:
        logging.debug('No value yet')
    else:
        logging.debug('value=%s', val)


def f(data):
    show(data)
    d.val = random.randint(1, 100)
    show(data)


class MyLocal(threading.local):
    def __init__(self, v=None):
        """
        To initialize the settings so all threads start with same value,
        subclass threading.local and set attributes in __init__()
        :param v:
        :return:
        """
        logging.debug('Initializing %r', self)
        self.val = v

if __name__ == '__main__':
    d = threading.local()
    show(d)
    d.val = 999
    show(d)

    for i in range(2):
        t = threading.Thread(target=f, args=(d,))
        t.start()
    # output: local_data.value is not set for any thread until it is set in that thread
    # (MainThread) No value yet
    # (MainThread) value=999
    # (Thread-1) No value yet
    # (Thread-1) value=51
    # (Thread-2) No value yet
    # (Thread-2) value=19
