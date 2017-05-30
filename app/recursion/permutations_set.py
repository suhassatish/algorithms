"""
Print all permutations of a given set
|S| = n
    2,7,4

{(2,4,7), (2,7,4), (4,2,7), (4,7,2), (7,2,4), (7,4,2)}
6 permutations = 3! = 3*2
Question asked in LinkedIn telephonic interview in Dec, 2014

def printPerm(set s, perm p):
    if set.isEmpty():
        print perm
        return

    for (e in s):
        s.remove(e)
        p.append(e)
        printPerm(s,p)
        p.remove_last() // in java, you cant iterate over a set while removing elements
        s.add(e)

Tip: build a different object in every leaf

|perm|i|set|

Invariant: program can never run faster than size of its output.
But same is not true for input. Sometimes, programs can run faster than the
input if they dont care and can discard some input. eg - binary search, or to print
only the first element of input

Use the pattern: build on the way down, do the work in the leaf.
The other way round(ie get the items from children, then prepend curr_node's result)
 works in theory, but takes O(n* n!) space, so its unacceptable


problem variant: print all permutations that satisfy a certain condition
have an isValid() check.

Concept of backtracking: Try to walk in a maze. Check at every step if that step is good.
If not good, then dont continue.
Pattern:
loop over all your options
make the step
check if step was good
only if step was good, make recursive call.

If without pruning tree, its exponential, even after pruning, it may still be exponential.
But it may be difficult to prove it.
In real life, smart pruning decides if program can run in reasonable time or not.
"""


def permutations(a):
    """
    The time complexity is O(n * n!) since there are n! permutations and we spend O(n) time to store
    each one.
    To prove there are n! permutations, the recursive relation is C(n) = n C(n - 1) + 1
    where n is due to the for loop within the recursive function.
    :param a:
    :return:
    """
    result = []
    _permutations(a, 0, result)
    return result


def _permutations(a, i, result):
    if i == len(a):
        result.append(list(a))
        return

    for j in xrange(i, len(a)):
        a[i], a[j] = a[j], a[i]
        _permutations(a, i + 1, result)  # generates all permutations for sublist a[i:]
        a[i], a[j] = a[j], a[i]

if __name__ == "__main__":
    print permutations([1, 2, 3])
    # [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
