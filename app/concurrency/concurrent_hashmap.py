"""
Implement a concurrent hash-map using lock striping.
Note: Apply a locking strategy that offers better concurrency and scalability.
Instead of synchornizing every method on a common lock, restricting access to a single thread at a
time, utilize a fine-grained locking mechanism called lock striping to allow a greater degree of
shared access.
"""