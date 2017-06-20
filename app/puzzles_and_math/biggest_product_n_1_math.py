import functools
import sys
import random


# @include
def find_biggest_n_minus_one_product(A):
    number_of_negatives = 0
    least_nonnegative_idx = least_negative_idx = greatest_negative_idx = None

    # Identify the least negative, greatest negative, and least nonnegative
    # entries.
    for i, e in enumerate(A):

        if e < 0:  # e is a negative-element
            number_of_negatives += 1

            # update least-negative-index
            if least_negative_idx is None or A[least_negative_idx] < e:
                least_negative_idx = i

            # update greatest-negative-index
            if greatest_negative_idx is None or e < A[greatest_negative_idx]:
                greatest_negative_idx = i

        else:  # element >= 0.
            if least_nonnegative_idx is None or e < A[least_nonnegative_idx]:
                least_nonnegative_idx = i

    if number_of_negatives % 2 == 1:  # odd-number of negatives, full_product will be negative
        idx_to_skip = least_negative_idx

    else:  # even-number of negatives (could also be 0 => all >= 0), full_product will be >= 0

        if least_nonnegative_idx is not None:  # has at least 1 element >= 0
            idx_to_skip = least_nonnegative_idx

        else:  # all -ve elements
            idx_to_skip = greatest_negative_idx

    # idx_to_skip = (least_negative_idx
    #                if number_of_negatives % 2 else least_nonnegative_idx if
    #                least_nonnegative_idx is not None else greatest_negative_idx)
    # return functools.reduce(lambda product, e: product * e,
    #                         # Use a generator rather than list comprehension to
    #                         # avoid extra space.
    #                         (e for i, e in enumerate(A) if i != idx_to_skip), 1)  # 1 is init val
    return product_minus_skip_index(A, idx_to_skip)
# @exclude


def product_minus_skip_index(A, idx_to_skip):
    prod = 1
    for i, e in enumerate(A):
        if i != idx_to_skip:
            prod *= e
    return prod


def check_ans(A):
    """
    # n^2 checking using brute force solution.
    Takes product of all numbers except A[i], and then iterates i from 0 to len(A) - 1
    Max of all these products is the max_prod
    :param A:
    :return:
    """
    max_product = float('-inf')
    for i in range(len(A)):
        product = 1
        for j in range(i):
            product *= A[j]
        for j in range(i + 1, len(A)):
            product *= A[j]
        if product > max_product:
            max_product = product
    print(max_product)
    return max_product


def main():
    for _ in range(10000):
        n = int(sys.argv[1]) if len(sys.argv) == 2 else random.randint(2, 11)
        A = [random.randint(-9, 9) for _ in range(n)]
        # print(*A)
        res = find_biggest_n_minus_one_product(A)  # A = [-8, 6, 1, 4, 7, -7, 7, -7, 3]
        print(res)
        assert res == check_ans(A)


if __name__ == '__main__':
    main()
