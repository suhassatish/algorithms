"""
Given an array of integers and a target integer K, find if there are a group of integers,
not necessarily contiguous, that can sum to K.

eg - [2,4,8], 6 -> True since 2+4 = 6
[2,-4,8], 1 -> False
[2,4,8], 14 -> True since 2+4+8 = 14
[2,4,8], 9 -> False

Brute force approach 1:
We can choose just 1 number that sums to K, (can choose in N ways in an N-element array)
or 2 numbers that sum to K, can choose in NC2 ways
...
or n - 1 numbers that sum to K, can choose in N C (N-1) ways

So in brute force solution, there are NC1 + NC2 + NC3 + ... NC (N-1) ways

Brute force approach 2:
Find all subsets of a set. There are 2^k of them, then filter the subsets that sum to K.

Back tracking optimization: If a subset_sum has already exceeded target, then discard that subset
and all containing those. Tree pruning.

http://www.geeksforgeeks.org/dynamic-programming-subset-sum-problem/
Partitioning a set of integers into K non-zero partitions to evaluate to a target is a well-known
NP-complete problem. There are no known polynomial-time solutions. Best you can do is use DP
to get a pseudo-polynomial time solution.

TODO:
1) Code the dynamic programing solution.

2) Solve a variant of this problem, asked in Google and Facebook interview
http://www.geeksforgeeks.org/find-subarray-with-given-sum/

2) Return the integers that sum to the target - iterative solution here
http://stackoverflow.com/questions/18305843/find-all-subsets-that-sum-to-a-particular-value
"""


def is_subset_sum(input_list, target):
    return _is_subset_sum(input_list, len(input_list), target)


def _is_subset_sum(input_list, num_elements_remaining, remaining_target):
    # import ipdb; ipdb.set_trace()
    if remaining_target == 0:
        return True
    if num_elements_remaining == 0 and remaining_target != 0:
        return False

    # early exit optimization
    # if last array element is greater than sum then ignore it
    # if input_list[num_elements_remaining - 1] > sum:
    #    num_elements_remaining -= 1

    # check if sum can be obtained by either including OR excluding the last element
    last_element = input_list[num_elements_remaining - 1]
    return (_is_subset_sum(
        input_list,
        num_elements_remaining - 1,
        remaining_target - last_element
        # numbers_so_far.add(last_element)
    ) or
            _is_subset_sum(
        input_list,
        num_elements_remaining - 1,
        remaining_target
        # numbers_so_far
    )
            )


if __name__ == '__main__':
    print(is_subset_sum([2,4,8], 6))   # True since 2+4 = 6
    print(is_subset_sum([2,-4,8], 1))  # False
    print(is_subset_sum([2,4,8], 14))  # True since 2+4+8 = 14
    print(is_subset_sum([2,4,8], 9))  # False
