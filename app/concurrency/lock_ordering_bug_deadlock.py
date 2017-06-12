"""
Demonstrate a lock-order deadlock using a code example and then induce simple lock ordering to avoid
the deadlock. Note: Think of threads as the nodes of a directed graph whose edges represent the
relation "Thread A waiting for resource held by Thread B". If this graph is cyclical, there is a
deadlock. This is likely to happen if 2 threads attempt to acquire the same set of locks in a
different order.

thread0 - lock_a; lock_b
thread1 - lock_b; lock_a

throw deadlock_detection_exception in production

have multiple layers of locks -
db_lock
fs_lock
kernel_lock

Deadlock detector -
approach 1:
Different systems (os_kernel, fs, db) calls its variety of locks.

approach 2:
Each time a new lock is required, you add it to a stack.
Then you merge all stacks (db_lock_stk, fs_lock_stk, kernel_lock_stk), then do topological sort
of all stacks to detect cycles with DFS.

"""

import time
import threading


# @include
class Account:

    _global_id = 0

    def __init__(self, balance):
        self._balance = balance
        self._id = Account._global_id
        Account._global_id += 1
        self._lock = threading.RLock()

    def get_balance(self):
        return self._balance

    @staticmethod
    def transfer(acc_from, acc_to, amount):
        th = threading.Thread(target=acc_from._move, args=(acc_to, amount))
        th.start()

    def _move(self, acc_to, amount):
        with self._lock:
            if amount > self._balance:
                return False
            acc_to._balance += amount
            self._balance -= amount
            print('returning True')
            return True
# @exclude


def main():
    acc_from = Account(200)
    acc_to = Account(100)
    print('initial balances =', acc_from.get_balance(), acc_to.get_balance())
    assert (acc_from.get_balance(), acc_to.get_balance()) == (200, 100)
    Account.transfer(acc_from, acc_to, 50)
    time.sleep(0.1)
    print('new balances =', acc_from.get_balance(), acc_to.get_balance())
    assert (acc_from.get_balance(), acc_to.get_balance()) == (150, 150)


if __name__ == '__main__':
    main()
