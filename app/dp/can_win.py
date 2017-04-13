# canWin
# board = [0, 3, 1, 2, 3, 0, 10]
# goal: move to value 0 cell.
# if value > 0, you can jump left or right by (value) steps
# if there exists a path ---> value 0 cell, we can win
# boolean "canWin" value whether there exists such a path
# given a board, startIndex, return the canWin


def can_win(a, start_index):
    visited = [False] * len(a)
    return _can_win(a, start_index, visited)


def _can_win(a, index, visited):

    if a[index] == 0:
        return True

    left_ret_value = right_ret_value = False

    left_index = index - a[index]
    right_index = index + a[index]

    if valid(a, left_index) and not visited[left_index]:
        visited[left_index] = True
        left_ret_value = _can_win(a, left_index, visited)

    if valid(a, right_index) and not visited[right_index]:
        visited[right_index] = True
        right_ret_value = _can_win(a, right_index, visited)

    if left_ret_value or right_ret_value:
        return True

    return False


def valid(a, index):
    if 0 <= index < len(a):
        return True
    else:
        return False

if __name__ == '__main__':
    board = [0, 3, 1, 2, 3, 0, 10]
    print can_win(board, 3)  # True

    board = [1, 3, 1, 2, 3, 1, 10]  # no 0 at all
    print can_win(board, 3)  # False

    board = [1, 3, 1, 2, 3, 1, 0]  # 0 reachable on right recursive subtree
    print can_win(board, 3)  # True

    board = [10, 0, 1, 2, 3, 1, 10]  # 0 reachable on left recursive subtree
    print can_win(board, 3)  # True

    board = [0, 10, 1, 2, 3, 1, 10]  # 0 not reachable at all
    print can_win(board, 3)  # False
