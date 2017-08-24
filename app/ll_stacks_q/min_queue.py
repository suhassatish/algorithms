"""
Q

DeQ

t1
Q: <- [1, 6, 4, 5] <-

maintain auxillary DeQ for min value

For each element, in aux deQ,
Either enq & deq backwards
or enq & deq forwards.

So 4N operations for N elements, ie O(4) for each element = amortized constant time

http://www.keithschwarz.com/interesting/code/?dir=min-queue
"""