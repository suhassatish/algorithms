"""
Boggle solver - Asked in Netflix onsite interview in June 2017

Optimal solution is using Trie and DFS -
https://stackoverflow.com/questions/746082/how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-solver/746102#746102

Example input -
Given a dictionary of word_list = ["geeks", "for", "quiz", "go"], and the current face of boggle cube with some letters,
boggle = [['G', 'I', 'Z'], ['U', 'E', 'K'], ['Q', 'S', 'E']]
is_word(str) returns True if str is present in dictionary, else false.

Output: Following words from boggle face are dictionary words - GEEKS, QUIZ

Inefficient solutions (compared to Trie)-
http://www.geeksforgeeks.org/boggle-find-possible-words-board-characters/

"""


grid = "fxie amlo ewbx astu".split()
nrows, ncols = len(grid), len(grid[0])

# A dictionary word that could be a solution must use only the grid's
# letters and have length >= 3. (With a case-insensitive match.)
import re
alphabet = ''.join(set(''.join(grid)))
bogglable = re.compile('[' + alphabet + ']{3,}$', re.I).match

words = set(word.rstrip('\n') for word in open('words') if bogglable(word))
prefixes = set(word[:i] for word in words
               for i in range(2, len(word)+1))


def solve():
    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            for result in extending(letter, ((x, y),)):
                yield result


def extending(prefix, path):
    if prefix in words:
        yield prefix, path
    for (nx, ny) in neighbors(path[-1]):
        if (nx, ny) not in path:
            prefix1 = prefix + grid[ny][nx]
            if prefix1 in prefixes:
                for result in extending(prefix1, path + ((nx, ny),)):
                    yield result


def neighbors(x, y):
    for nx in range(max(0, x-1), min(x+2, ncols)):
        for ny in range(max(0, y-1), min(y+2, nrows)):
            yield nx, ny