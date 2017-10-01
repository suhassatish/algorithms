"""
Some start-ups are enamored by skip lists.
http://igoro.com/archive/skip-lists-are-fascinating/

---------
https://stackoverflow.com/questions/256511/skip-list-vs-binary-tree
1) Locking skip lists are insanely fast. They scale incredibly well with the number of concurrent accesses.
This is what makes skip lists special, other lock based data structures tend to croak under pressure.

2) Lock-free skip lists are consistently faster than locking skip lists but only barely.

3) Transactional skip lists are consistently 2-3 times slower than the locking and non-locking versions.

4) Locking red-black trees croak under concurrent access.
Their performance degrades linearly with each new concurrent user.
Of the two known locking red-black tree implementations, one essentially has a global lock during tree rebalancing.
The other uses fancy (and complicated) lock escalation but still doesn't significantly out perform the global lock
version.

5) Lock-free red-black trees don't exist (no longer true, see Update).

6) Transactional red-black trees are comparable with transactional skip-lists.
That was very surprising and very promising. Transactional memory, though slower is far easier to write.
It can be as easy as quick search and replace on the non-concurrent version.

"""