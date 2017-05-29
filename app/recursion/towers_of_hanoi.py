"""
http://www.cs.cmu.edu/~cburch/survey/recurse/hanoiimpl.html
Also in EPI 16.1 under recursion chapter, page 260 in version 2 of Java book.

The time complexity recurrence relation is
T(n) = T(n - 1) + 1 + T(n - 1)
     = 2T(n - 1) + 1
     = O(2**n)
"""
NUM_PEGS = 3


def compute_towers_hanoi(num_rings):
    """
    The default number of stands (aka pegs) in classical towers of hanoi = 3.
    This is assumed.
    :param num_rings: The total number of rings to be moved from 1 peg (src) to the destination peg
    with the constraint that the larger rings always appear below the smaller rings.
    :return:
    """
    pegs = []

    # create 3 separate lists - for source, destination, and spare
    # Its a mistake to create lists as [list()] * 3, this will create 3 references to the same
    # single list under the hood. Hence, need to create lists with for-loop like below
    for i in xrange(NUM_PEGS):
        pegs.append(list())
    for ring in xrange(num_rings, 0, - 1):  # desc order of size (size = ring_number here)
        pegs[0].append(ring)  # will look like src_peg = [5, 4, 3, 2, 1]

    _compute_towers_hanoi_steps(pegs, num_rings, 0, 1, 2)


def _compute_towers_hanoi_steps(pegs, num_rings_to_move, src_peg, dest_peg, spare_peg):
    """

    :param pegs:
    :param num_rings_to_move:
    :param src:
    :param dest:
    :param spare:
    :return:
    """
    if num_rings_to_move > 0:
        _compute_towers_hanoi_steps(pegs, num_rings_to_move - 1, src_peg, spare_peg, dest_peg)
        pegs[dest_peg].append(pegs[src_peg].pop())
        _compute_towers_hanoi_steps(pegs, num_rings_to_move - 1, spare_peg, dest_peg, src_peg)
