# print "Hello, world!"
# fixed size queue , allocated capacity upfront; then the capacity shouldn't change at all;
# methods - put , get; unit tests;
# multiple-threads


class Queue(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.q = [None] * capacity
        self.head = 0
        self.tail = 0
        self.n = 0

    def get(self):
        """
        gets from the head of the queue, returns an item of the same data type as contents
        in the queue. Like deque
        """
        if self.is_empty():
            raise Exception("Queue empty")
        self.n -= 1
        val = self.q[self.head]
        # self.q[self.head] = None  # removes dangling reference, helps garbage collection
        self.head = (self.head + 1) % self.capacity
        return val

    def put(self, val):
        """
        Raises an exception if queue is full. Returns None
        """
        if self.n == self.capacity:
            raise Exception("Queue full")
        self.q[self.tail] = val
        self.tail = (self.tail + 1) % self.capacity
        self.n += 1
        return

    def is_empty(self):
        return True if self.n == 0 else False


if __name__ == '__main__':
    q = Queue(5)
    q.put(1)
    q.put(-1)
    q.put(None)
    q.put(123)
    q.put('a')
    try:
        q.put(34) # should raise is_full exception.
        raise Exception("should not be here")
    except Exception, e:
        pass
    print q.get()
    print q.get()
    print q.get()
    print q.get()
    print q.get()
    try:
        q.get() # should raise is_empty exception
        raise Exception("should not be here")
    except Exception, e:
        pass

    q.put('wrap')
    print q.get()
