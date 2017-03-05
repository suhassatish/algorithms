"""
In an arbitrary tree, the distance between 2 most distant vertices
is the diameter of the tree

Each recursive frame (node) has to answer 2 questions -
1) what is my max_diameter aka,
   sum of distances to two most distant leaves from different children.
2) what is the distance to my most distant leaf


http://www.geeksforgeeks.org/diameter-of-a-binary-tree/

O(n) time and O(n) space
"""


class TreeNode(object):
    # Constructor to create a new node
    def __init__(self):
        self.dist_from_parent = None
        self.children = None
        self.farthest_leaf_dist = None
        self.diameter = None


class EdgeWeightedTree(object):
    def __init__(self, string):
        self.index = 0
        self.string = string
        self.root = self.build_tree(string)

    def build_tree(self, string):
        """
        Takes O(N) time to construct it
        :param string:
        :return:
        """
        return self._build_tree(string)

    def _build_tree(self, string):
        """
        Reads a string like "{0,1,{5,1,{4,1,{7,0}}}}"
        and builds a tree out of it.
        The format is {edge_wt, num_children, {same info for each child}}
        :param string:
        :param index: index in the string
        :return: A tree like this in above example
              root
              /5
          Child1
            /4
          Child2
          /7
         Child3
        """
        self.index += 1  # ignore leading '{'
        node = TreeNode()
        node.dist_from_parent = self.read_number(string)
        self.index += 1  # ','
        num_children= self.read_number(string)
        self.index += 1  # ',' or '}'
        if num_children == 0:
            return node
        node.children = []  # list of TreeNodes

        while num_children > 0:
            node.children.append(self._build_tree(string))
            num_children -= 1
            self.index += 1
        return node

    def read_number(self, string):
        """
        Returns number of children by parsing a tree string structure
        :param string:
        :param index: Index in the string
        :return:
        """
        d = 0
        while string[self.index].isdigit():
            d *= 10
            d += int(string[self.index])
            self.index += 1
        return d

    def get_diameter(self):
        """
        Function to get the diamter of an EdgeWeighted arbitrary tree
        """

        # Base Case when tree is empty
        if self.root is None:
            return None

        self._get_diameter(self.root)
        return self.root.diameter

    def _get_diameter(self, node):
        """
        Each recursive frame (node) has to answer 2 questions -
        1) what is my max_diameter aka,
            sum of distances to two most distant leaves from different children.
        2) what is the distance to my most distant leaf

        We return this by adding this info to 2 additional fields added to TreeNode class,
        diameter and farthest_leaf_dist
        """
        if node.children is None:
            node.diameter = 0
            node.farthest_leaf_dist = node.dist_from_parent
            return

        node.diameter = -1

        # these variables help us achieve linear time solution
        farthest_leaf_dist = second_farthest_leaf_dist = 0
        for child in node.children:
            self._get_diameter(child)  # this computes the child's diameter, farthest_leaf_dist
            node.diameter = max(node.diameter, child.diameter)

            if child.farthest_leaf_dist > farthest_leaf_dist:
                second_farthest_leaf_dist = farthest_leaf_dist
                farthest_leaf_dist = child.farthest_leaf_dist

            elif child.farthest_leaf_dist > second_farthest_leaf_dist:
                second_farthest_leaf_dist = child.farthest_leaf_dist

        node.farthest_leaf_dist = farthest_leaf_dist + node.dist_from_parent
        node.diameter = max(node.diameter, farthest_leaf_dist + second_farthest_leaf_dist)
        return
