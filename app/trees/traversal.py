from collections import deque


def dfs_recursive(root):
    if root is None:
        return
    else:
        print(root.val)
        dfs_recursive(root.left)
        dfs_recursive(root.right)


def dfs_iterative(root):
    stk = []
    stk.push(root)

    while not stk.empty():
        node = stk.pop()

        if node is None:
            return

        else:
            print(root.val)
            if root.left is not None:
                stk.append(root.left)

            if root.right is not None:
                stk.append(root.right)


def bfs(root):
    q = deque()

    if root is None:
        return
    q.append(root)

    while q:
        print(node.val)
        node = q.popleft()
        if node.left is not None:
            q.append(node.left)
        if node.right is not None:
            q.append(node.right)
