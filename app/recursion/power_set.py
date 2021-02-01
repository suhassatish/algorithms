"""
Find all subsets of a given set
There are 2^n subsets in a given set

{2,7,3} = {2,7,3}, {2,7}, {2,3}, {7,3}, {2}, {7}, {3}, {}

# https://www.quora.com/What-is-the-recursive-solution-for-finding-all-subsets-of-a-given-array

Very important idiom in recursion:
neighboring recursive node sees a smaller view of the world

Space is O(n)
Tree is complete binary tree, so there are 2^n subsets

Every subset can be represented as an n-dimensional binary vector
where n = cardinality of set (number of elements)

Lets do some time complexity analysis to list all subsets of a set having 64 elements
If set has 64 elements, it has 2^64 subsets
Even if you can compute 2^30 (1 Billion subsets) subsets/sec, total takes
2^34 sec
2^12 sec/hr
2^32 hours in 1 day,  assuming for simplicity that there are 32 hours/day

so it takes 2^17 days
even if there are 512 days/yr = 2^9 => 2^8 years = 256 years

So doesnt make sense to go over all the subsets of a set of size 64.


Intuition of recursive relationship:
power_set of {1,2,3} - removes 3 and calls power_set on {1,2}.
    power_set of {1,2} - removes 2 and calls power_set on {1}
        power_set of {1} - removes 1 and calls power_set on {}
            power set of {} returns {{}}
        takes child ret_val and adds it to the set, then adds 1 to all elements to get {{}, {1}}
    takes child ret_val and adds 2 to all elements {{}, {1}, {2}, {1,2}}
takes child ret_val and adds 3 to all elements {{},    {1},   {2},   {1,2},
                                                {3}, {1,3}, {2,3}, {1,2,3}}

Additional notes: Also refer EPI 2.0 problem 16.4 under recursion chapter, gen power_set
Key concept: Bit manipulation. The power set is the list of set bits in the set of integers
 from 0 to (2^n - 1) where 0 indicates element at index i doesnt exist in set and 1 indicates its
 presence. Example power set of {1,2,3} - {{}, {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}}
can be represented by bit-vector from
[000, 001, 010, 011, 100, 101, 110, 111] which are integer from 0 to 2^3 - 1

To get the lowest set bit of x, y = x & ~(x-1).

To get the index of the set bit, lg(y). Using this you can compute power_set in O(n*2^n) but is
very fast due to bit manipulation.
Space complexity if you store all elements is
total num_subsets (2^n) * avg_size of a subset (n/2) = n * 2^n
Instead, if you just print instead of storing, its the depth of the recursion stack = O(n)
"""


def power_set(input_list):
    """
    Implementation detail:
    In python, list, dict and set are mutable (not hashable). So the keys in a dict or set should
    always be immutable (hashable). This means that you cannot have a set of sets in python.
    Or a set of lists or a set of dicts.
    You will get TypeError: unhashable type: 'set'
    To circumvent this issue, you can have a set of frozensets, since a frozenset is immutable
    and hence hashable.
    :param input_list:
    :return:
    """
    deduped_input_list = list(set(input_list))
    output_list = [[]]
    curr_list = []
    _power_set(deduped_input_list, 0, curr_list, output_list)
    return output_list


def _power_set(input_list, index, selected_so_far, output_list):
    """
    Using lists here for ease of indexing elements, thats not easy in a set as set is unordered
    collection.
    :param input_list:
    :param index:
    :param curr_list:
    :param output_list:
    :return:
    """
    if index == len(input_list):

        #  Note: If you dont create a new list here, it returns a list of size 2^n of all []
        # the reason is that its just referencing the list from previous stack frame which
        # eventually becomes []
        output_list.append(list(selected_so_far))
        return

    selected_so_far.append(input_list[index])

    #  generate all sets that contain input_list[index]
    _power_set(input_list, index + 1, selected_so_far, output_list)

    selected_so_far.pop()

    # generate all sets that do not contain input_list[index]
    _power_set(input_list, index + 1, selected_so_far, output_list)


if __name__ == '__main__':
    for i in power_set([2, 7, 3, 2]):
        print(i)
