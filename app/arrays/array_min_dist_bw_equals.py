"""
Consider an array of  integers, . The distance between two indices,  and , is denoted by .

Given , find the minimum  such that  and . In other words, find the minimum distance between any pair of equal elements
in the array. If no such value exists, print .

Note:  denotes the absolute value of .

Input Format

The first line contains an integer, , denoting the size of array .
The second line contains  space-separated integers describing the respective elements in array .

Constraints

Output Format

Print a single integer denoting the minimum  in ; if no such value exists, print .

Sample Input

6
7 1 3 4 1 7
Sample Output

3
Explanation
Here, we have two options:

7 has indices 0 and 5
1 has indices 1 and 4, so min distance is 3
The answer is 3.
"""


def find_min_distance_bw_equals(n, A):

    # invalid input or array of size 1
    if n <= 1 or len(set(A)) == n or len(A) != n:
        return -1

    # all distinct array elements, no duplicates
    elif len(set(A)) == n:
        return -1

    else:
        inverted_index_dict = {}
        for index, element in enumerate(A):
            if element in inverted_index_dict:
                stored_index, stored_distance = inverted_index_dict[element]
                new_distance = index - stored_index
                if stored_distance == -1 or new_distance < stored_distance:
                    inverted_index_dict[element] = (index, new_distance)
            else:
                inverted_index_dict[element] = (index, -1)
        print("inverted_index_dict = %s", repr(inverted_index_dict))
        return _find_min_distance_from_dict(inverted_index_dict)


def _find_min_distance_from_dict(d):
    distances = [t2 for t1,t2 in d.values()]
    return min(filter(positive, distances))


def positive(element):
    return element > 0


if __name__ == "__main__":
    n = int(input().strip())
    A = map(int, input().strip().split(' '))
    print(find_min_distance_bw_equals(n, A))




