"""
https://stackoverflow.com/questions/8871204/count-number-of-1s-in-binary-representation

We're given a large array of 4-byte integers. We need to find out how many total bits are turned on (1s are set).
Such a digital sum of binary representation of a number is called its Hamming Weight.

eg - If input array has 2 numbers [31, 51], answer is 9 because
31 has 5 bits set and
51 has 4 bits set, so
5 + 4 = 9

Solution is fast using extra memory without any bit-hackery. No floating points, base-10.

"""