"""
This is a variant of the classical knight's tour problem.
Given starting and ending co-ordinates of a knight on a chess board, calculate the shortest number
of moves that a knight can take to get there.

Input:
rows
cols
startx
starty
endx
endy

Output -1 if there is no solution. or num = integer >= 0.

Hint:
http://stackoverflow.com/questions/2339101/knights-shortest-path-chess-question

The goal is to find the shortest path from (x0,y0) to (x1,y1)
using only the candidate steps (+-1, +-2), (+-2, +-1),

Without the trouble of defining nodes and edges, the below dynamic programing formula may also work
NumWays(x,y)= 1+ min(NumWays(x+-2,y-+1),NumWays(x+-1,y+-2));
"""
from collections import deque
from bfs import BreadthFirstPaths
from graph_api import Graph


def min_knight_moves(rows, cols, startx, starty, endx, endy):
    b = Board(rows, cols, startx, starty, endx, endy)
    return b.get_minimum_moves()


class Board(object):

    def __init__(self, rows, cols, startx, starty, endx, endy):
        self.rows = rows
        self.cols = cols
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.graph = Graph(rows * cols)
        self.visited = [[False for _ in xrange(cols)] for r in xrange(rows)]
        q = deque()
        q.append((startx, starty))
        self.visited[startx][starty] = True
        while q:
            x, y = q.popleft()
            neighbors = self.next_knight_squares_from(x, y)
            for r, c in neighbors:
                self.graph.add_edge(self.get_vertex_id(x, y), self.get_vertex_id(r, c))
                if not self.visited[r][c]:
                    self.visited[r][c] = True
                    q.append((r, c))

    def get_minimum_moves(self):
        """
        this gets the minimum knight moves from (startx, starty) -> (endx, endy)
        :return:
        """
        # short circuit and return if end_cell not reachable
        if not self.visited[self.endx][self.endy]:
            return -1
        else:
            bfp = BreadthFirstPaths(self.graph, self.get_vertex_id(self.startx, self.starty))
            return bfp.dist_to[self.get_vertex_id(self.endx, self.endy)]

    def next_knight_squares_from(self, curr_row, curr_col):
        """
        :param curr_row:
        :param curr_col:
        :return: returns a list of valid (i,j) co-ordinates where a knight can move, given
        its starting co-ordinates as (curr_row, curr_col) on a rectangular board of dimension
        rows x cols
        """
        next_moves = [(curr_row + 2, curr_col + 1), ([curr_row + 2, curr_col - 1]),
                      (curr_row - 2, curr_col + 1), ([curr_row - 2, curr_col - 1]),
                      (curr_row + 1, curr_col + 2), ([curr_row + 1, curr_col - 2]),
                      (curr_row - 1, curr_col + 2), ([curr_row - 1, curr_col - 2])]
        valid_next_moves = filter(self.valid, [(i, j) for i, j in next_moves])
        return valid_next_moves

    def valid(self, coordinates):
        curr_row, curr_col = coordinates[0], coordinates[1]
        if 0 <= curr_row < self.rows and 0 <= curr_col < self.cols:
            return curr_row, curr_col

    def get_vertex_id(self, i, j):
        """
        returns the index in a 1-dimensional array-index that represents the graph nodes
        :param j:
        :param i:
        :param cols:
        :return: vertex_id which is an integer
        """
        return self.cols * i + j

if __name__ == '__main__':
    print min_knight_moves(3, 3, 0, 0, 2, 2)  # 4
    print min_knight_moves(8, 8, 0, 0, 7, 7)  # 6
    print min_knight_moves(16, 16, 4, 3, 12, 13)  # 6
    print min_knight_moves(64, 64, 4, 3, 56, 56)  # 35
    print min_knight_moves(64, 64, 11, 14, 56, 62)  # 31
