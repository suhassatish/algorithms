"""
Fastest way for string operations on N  k-length string

                hashSet       SortedArray    Trie
search          O(k)(hashing)  O(k lg N)      O(k)
insert          O(k)           O(N)           O(k)
delete          O(k)           O(N)           O(k)


                               N + sigma(Ki)
storage space   O(~40N)        most efficient  an array of size character set for each node

prefix lookup   O(Nk)           O(k lg N)       O(k)
           loop-over-collection

Trie is heavy and space inefficient to store. 1K per node.
Hence rarely used in practice. But frequently asked in interviews.

Given a set of strings W, return all indexes i,j
such that i != j and W[i] concat W[j] is a palindrome.

{'bo', 'b', 'abcd', 'cba'} => 0,1 because bob is a palindrome; abcdcba is a palindrome
Brute force = O(N^2 * k)

In a general case, Wi = reversed(Wj) +  a palindrome

Build a trie of the reverse of the smaller string.
When trie announces that its a prefix and has reached the end of the word,
now check the rest of the word if its a palindrome.

Worst case input = {a, aa, aaa, aaaa, aaaaa, ...}

(n - k/2) * k/2 * k/2

Compact tries.
Add an illegal $ symbol at the end of each word.
cat$, cow$, dog$, doggy$
This ensures dog$ is not a prefix of doggy$

Every word can fork 1 node. At most 2n nodes.
Each word can have at-most n-1 internal nodes.
Whats the space for a compact trie?
Now the edges take substrings, the edges altogether take N * k space.


Possible to achieve - 2N edges, 2N nodes and each edge takes constant space.
"""


class Node(object):
    def __init__(self, label=None, data=None):
        self.label = label
        self.data = data
        self.children = dict()

    def add_child(self, key, data=None):
        if not isinstance(key, Node):
            self.children[key] = Node(key, data)
        else:
            self.children[key.label] = key

    def __getitem__(self, key):
        return self.children[key]


class Trie(object):
    def __init__(self):
        self.head = Node()

    def __getitem__(self, key):
        return self.head.children[key]

    def add(self, word):
        current_node = self.head
        word_finished = True

        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_finished = False
                break

        # For ever new letter, create a new child node
        if not word_finished:
            while i < len(word):
                current_node.add_child(word[i])
                current_node = current_node.children[word[i]]
                i += 1

        # Let's store the full word at the end node so we don't need to
        # travel back up the tree to reconstruct the word
        current_node.data = word

    def has_word(self, word):
        if word == '':
            return False
        if word is None:
            raise ValueError('Trie.has_word requires a not-Null string')

        # Start at the top
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break

        # Still need to check if we just reached a word like 't'
        # that isn't actually a full word in our dictionary
        if exists:
            if current_node.data is None:
                exists = False

        return exists

    def start_with_prefix(self, prefix):
        """ Returns a list of all words in tree that start with prefix """
        words = list()
        if prefix is None:
            raise ValueError('Requires not-Null prefix')

        # Determine end-of-prefix node
        top_node = self.head
        for letter in prefix:
            if letter in top_node.children:
                top_node = top_node.children[letter]
            else:
                # Prefix not in tree, go no further
                return words

        # Get words under prefix
        if top_node == self.head:
            queue = [node for key, node in top_node.children.iteritems()]
        else:
            queue = [top_node]

        # Perform a breadth first search under the prefix
        # A cool effect of using BFS as opposed to DFS is that BFS will return
        # a list of words ordered by increasing length
        while queue:
            current_node = queue.pop()
            if current_node.data != None:
                # Isn't it nice to not have to go back up the tree?
                words.append(current_node.data)

            queue = [node for key,node in current_node.children.iteritems()] + queue

        return words

    def getData(self, word):
        """ This returns the 'data' of the node identified by the given word """
        if not self.has_word(word):
            raise ValueError('{} not found in trie'.format(word))

        # Race to the bottom, get data
        current_node = self.head
        for letter in word:
            current_node = current_node[letter]

        return current_node.data


if __name__ == '__main__':
    trie = Trie()
    words = 'hello goodbye help gerald gold tea ted team to too tom stan standard money'
    for word in words.split():
        trie.add(word)
    print(trie.has_word('goodbye'))
    print(trie.start_with_prefix('g'))
    print(trie.start_with_prefix('to'))
