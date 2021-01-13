"""
Multiple 2 sparse matrices. Make use of the sparsity given that most of the elements are 0s

The standard matrix multiplication takes approximately 2*N^3 (where N = 2n) arithmetic operations
(additions and multiplications); the asymptotic complexity is O(N^3).
[[a11, a12], [a21, a22]] * [[b11, b12, b13], [b21, b22, b21]]
    = [[c11, c12, c13], [c21, c22, c23], [c31, c32, c33]]
  [2 x 2] * [2 x 3] = [2 x 3]
c11 = R1[A] * C1[B] = a11*b11 + a12*b21
c12 = R1[A] * C2[B] = a11*b12 + a12*b22
c13 = R1[A] * C3[B] =

[[1, 0, 0], [-1, 0, 3]] * [[7, 0, 0], [0,0,0], [0,0,1]] = [[7,0,0], [-7, 0, 3]]

# strassen's algorithm = O(N^2.7) = most optimal solution; this takes care of sparse matrices;
# but it only makes it 10% faster than traditional matrix multiplication that too for matrices
# of size > 1k rows/columns

Optimized solution for sparsity - Keep a list of hash_sets for A with only indexes that are non-zero
elements in each row.
ie, For A, [hsA[r1], hsA[r2]]

For B, keep a column major list of hash_sets such that
[hsB[1], hsB[2], hsB[3]] = [hsB[col1], hsB[c2], hsB[c3]]
where B[c1] will be only non-zero elements of B's Column 1

This will only save on space, but not really save on time. Its still O(N^3)

http://www.geeksforgeeks.org/strassens-matrix-multiplication/
"""


def matrix_mult_naive(A, B):
    """

    :param A: M x N
    :param B: N x K
    :return: C of dimension M x K
    """
    C = [[0 for col in range(len(B[0]))] for row in range(len(A))]
    for row in range(len(A)):  # M
        for col in range(len(B[0])):  # K
            for k in range(len(A[0])):
                C[row][col] += A[row][k] * B[k][col]
    return C


if __name__ == '__main__':
    print(matrix_mult_naive([[1, 0, 0], [-1, 0, 3]], [[7, 0, 0], [0,0,0], [0,0,1]]))
    # [[7, 0, 0], [-7, 0, 3]]

