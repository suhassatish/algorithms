"""
Caterpillars eat leaves.
Given N leaves,
1,2,3,...N
and K caterpillars,
with random numbers, with repeats.

After all are done, how many leaves will remain?
Brute force solution = O(NK) . Go thru all N leaves, if its a multiple of any of them,
incremenet eaten_count.

Suppose k = 7,2,3,...
N/7 + N/2 + N/3 - N/(7*2) - N/(7*3) - N/(3*2) + N/(7*3*2)
|A u B u C| = |A| + |B| + |C| - |A ^ B| - |A ^ C| - |B ^ C| + |A ^ B ^ C|
this is called inclusion-exclusion principle

For odd, you include, for even you exclude, always.

Generate subsets of same size always. Then store them.

2^k subsets need to be generated at some point, this is unavoidable.
You also need the storage space for LCMs.
Brute force seems more efficient.
"""