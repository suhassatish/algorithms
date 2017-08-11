"""
There is a 2-dimensional grid where guards are patrolling a maze.
Where do you place a bomb such that you kill maximum bember of guards (enemy E)?
There can be walls W at certain spots which will block the spread of the bomb along that path.

eg -
|E|E| |
| |W| |
| |H|E|
| |E| |
solution - detonating bomb at H kills 2 guards, but doesnt kill guard behind wall W as wall
saves him.

Separate into 2 independent dimensions like n-queens problem reduced to 1-dimension.
hospiral kills (hkill) and vertical_kills (vkill), then kills[i][j] = hkill[i][j] + vkill[i][j]

Its 3 traversals of n-by-n grid
"""


class KillCount(object):
    count = 0


def hkill(grid):
    """
    :param grid: assume grid is n by n square
    :return:
    """
    n = len(grid)
    result = [[0 for j in len(grid[0])] for i in len(grid)]
    for r in xrange(n):
        kc = KillCount()
        for c in xrange(n):
            if grid[r][c] == 'E':
                kc.count += 1
            elif grid[r][c] == 'W':
                kc = KillCount()
            else:
                result[r][c] = kc
    return result
