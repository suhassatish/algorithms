"""
Implement a queue using exactly 2 stacks for integer values.
Ensure FIFO property, but stack has LIFO property.
Trick is to reverse stk1 by putting it into stk2

enq:  # O(1) time requirement; it is amortized O(1)
    s1.push(item)

deq:  # O(1) time requirement; it is amortized O(1)
    if s2.size != 0:
        s2.pop()
    else:
        while s1 is not empty():
            s2.push(s1.pop())
        s2.pop()

size:
    size(s1) + size(s2)
"""

