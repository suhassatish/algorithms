"""
Size-aware batch/value vector:
Drill keeps a list of chunks of 16MB. For allocation beyond 16MB, it
asks for system memory through netty. With each batch having 64k rows, if a
column width is beyond 256, value vector would requires > 16MB. Drill may
hit OOM, even if there are plenty of free chunk of 16MB.

Proposal to fix is to impose size constraint on value vector, by
providing a new set of setSafe() methods.
"""