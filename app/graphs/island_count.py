"""
Given a map 2D grid of 0 and 1
Where 0 = water, 1 = land, count the number of islands.


|0|1|1|0|0|
|1|1|0|0|1|
|0|0|1|1|0|
|0|1|0|0|0|

Iterate over the 2D matrix, do a DFS on each node.
Go to the next unvisited node and repeat the same. Count how many times you have to do it.

For implicit graph problems, dont create a graph of vertices.


"""


def count_islands(matrix):
    visited = [0 for i in xrange(len(matrix)) for j in xrange(len(matrix[0]))]
    count = 0
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[0])):
            if matrix[i][j] and visited[i][j] == 0:
                exhaust_cc(matrix, i, j, visited)
                count += 1


def exhaust_cc(grid, i, j, visited):
    if visited[i][j]:
        return

    visited[i][j] = 1
    for n in get_neighbors(grid, i, j):
        exhaust_cc(grid, n[0], n[1], visited)


def get_neighbors(grid, i, j):
    """
    Tip: (Hear say) Facebook doesnt care about memory,
    you can use how much ever additional memory you want. => Hint: Try using hash_maps if possible
    :param grid:
    :param i:
    :param j:
    :return:
    """
    possible = [(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)]
    neighbors = []

    for row, col in possible:
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
            neighbors.append((row, col))

    return neighbors
