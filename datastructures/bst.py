from datastructures.queue import LinkedListQueue


# TODO Only necessary for Python 3, check for that. Also, see if its possible
# to use Python 3's compare rules
def cmp(a, b):
    return (a > b) - (a < b)

class RedBlackBST(object):
    """A symbol table implemented using a left-leaning red-black BST."""
    RED = True
    BLACK = False

    root = None

    class Node(object):
        def __init__(self, key, value, color, N):
            self.key = key
            self.value = value
            self.color = color
            self.N = N
            self.left = None
            self.right = None

        def __str__(self):
            return '%s: %s' % (self.key, self.value)

    def is_red(self, node):
        if node is None:
            return False
        return node.color == self.RED

    def size(self):
        return self.size_node(self.root)

    def size_node(self, node):
        if node is None:
            return 0
        return node.N

    def is_empty(self):
        return self.root is None

    #
    # Standard BST search
    #
    def get(self, key):
        """Returns value associated to key, or None if key cannot be found."""
        return self.get_node(key, self.root)

    def get_node(self, key, node):
        while node is not None:
            compare = cmp(key, node.key)
            if compare < 0:
                node = node.left
            elif compare > 0:
                node = node.right
            else:
                return node.value

        return None

    def contains(self, key, node=None):
        """Does the BST contain a node with key?"""
        if node is None:
            return self.get(key) is not None
        else:
            return self.get_node(key, node) is not None

    #
    # Red-Black insertion
    #
    def put(self, key, value):
        self.root = self.put_node(key, value, self.root)
        self.root.color = self.BLACK
        assert self.check_integrity()

    def put_node(self, key, value, node):
        if node is None:
            return self.Node(key, value, self.RED, 1)

        compare = cmp(key, node.key)
        if compare < 0:
            node.left = self.put_node(key, value, node.left)
        elif compare > 0:
            node.right = self.put_node(key, value, node.right)
        else:
            node.value = value

        # Fix-up any right-leaning links
        if self.is_red(node.right) and not self.is_red(node.left):
            node = self.rotate_left(node)
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)

        node.N = self.size_node(node.left) + self.size_node(node.right) + 1

        return node

    #
    # Red-Black deletion
    #

    # Delete the key-value pair with the minimum key rooted at node
    def delete_min(self):
        if self.is_empty():
            raise ValueError('BST underflow')

        # If both children of root are black, set root to red
        if not self.is_red(self.root.left) and \
           not self.is_red(self.root.right):
            self.root.color = self.RED

        self.root = self.delete_min_node(self.root)

        if not self.is_empty():
            self.root.color = self.BLACK

    def delete_min_node(self, node):
        if node.left is None:
            return None

        if not self.is_red(node.left) and \
           not self.is_red(node.left.left):
            node = self.move_red_left(node)

        node.left = self.delete_min_node(node.left)

        return self.balance(node)

    # Delete the key-value pair with the maximum key rooted at node
    def delete_max(self):
        if self.is_empty():
            raise ValueError('BST underflow')

        # If both children of root are black, set root to red
        if not self.is_red(self.root.left) and \
           not self.is_red(self.root.right):
            self.root.color = self.RED

        self.root = self.delete_max_node(self.root)

        if not self.is_empty():
            self.root.color = self.BLACK

    def delete_max_node(self, node):
        if self.is_red(node.left):
            node = self.rotate_right(node)

        if node.right is None:
            return None

        if not self.is_red(node.right) and \
           not self.is_red(node.right.left):
            node = self.move_red_right(node)

        node.right = self.delete_max_node(node.right)

        return self.balance(node)

    def delete(self, key):
        if not self.contains(key):
            raise ValueError('Tree does not contain key %s' % key)

        # If both children of root are black, set root to red
        if not self.is_red(self.root.left) and \
           not self.is_red(self.root.right):
            self.root.color = self.RED

        self.root = self.delete_node(key, self.root)

        if not self.is_empty():
            self.root.color = self.BLACK

    def delete_node(self, key, node):
        if cmp(key, node.key) < 0:
            if not self.is_red(node.left) and \
               not self.is_red(node.left.left):
                node = self.move_red_left(node)

            node.left = self.delete_node(key, node.left)
        else:
            if self.is_red(node.left):
                node = self.rotate_right(node)

            if cmp(key, node.key) == 0 and node.right is None:
                return None

            if not self.is_red(node.right) and \
               not self.is_red(node.right.left):
                node = self.move_red_right(node)

            if cmp(key, node.key) == 0:
                node_min = self.min_node(node.right)
                node.key = node_min.key
                node.value = node_min.value
                node.right = self.delete_min_node(node.right)
            else:
                node.right = self.delete_node(key, node.right)

        return self.balance(node)

    #
    # Red-Black tree helper functions
    #

    # Make a left-leaning link lean to the right
    def rotate_right(self, node):
        assert node is not None and self.is_red(node.left)

        x = node.left
        node.left = x.right
        x.right = node
        x.color = x.right.color
        x.right.color = self.RED
        x.N = node.N
        node.N = self.size_node(node.left) + self.size_node(node.right) + 1
        return x

    # Make a right-leaning link lean to the left
    def rotate_left(self, node):
        assert node is not None and self.is_red(node.right)

        x = node.right
        node.right = x.left
        x.left = node
        x.color = x.left.color
        x.left.color = self.RED
        x.N = node.N
        node.N = self.size_node(node.left) + self.size_node(node.right) + 1
        return x

    # Flip the colors of a node and its two children
    def flip_colors(self, node):
        assert node is not None and node.left is not None and \
                node.right is not None
        assert (not self.is_red(node) and self.is_red(node.left) and
                self.is_red(node.right)) or \
                (self.is_red(node) and not self.is_red(node.left) and
                 not self.is_red(node.right))

        node.color = not node.color
        node.left.color = not node.left.color
        node.right.color = not node.right.color

    # Assuming that h is red and both h.left and h.left.left
    # are black, make h. or one of its children red.
    def move_red_left(self, node):
        assert node is not None
        assert self.is_red(node) and not self.is_red(node.left) and \
                not self.is_red(node.left.left)

        self.flip_colors(node)
        if self.is_red(node.right.left):
            node.right = self.rotate_right(node.right)
            node = self.rotate_left(node)

        return node

    # Assuming that h is red and both h.right and h.right.left
    # are black, make h.right or one of its children red.
    def move_red_right(self, node):
        assert node is not None
        assert self.is_red(node) and not self.is_red(node.right) and \
                not self.is_red(node.right.left)

        self.flip_colors(node)
        if self.is_red(node.left.left):
            node = self.rotate_right(node)

        return node

    # Restore red-black tree invariant
    def balance(self, node):
        assert node is not None

        if self.is_red(node.right):
            node = self.rotate_left(node)
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)

        node.N = self.size_node(node.left) + self.size_node(node.right) + 1

        return node

    #
    # Utility functions
    #
    def height(self):
        return self.height_node(self.root)

    def height_node(self, node):
        if node is None:
            return 0

        return 1 + max(self.height_node(node.left), self.height_node(node.right))

    #
    # Ordered symbol table methods
    #
    def min(self):
        if self.is_empty():
            return None
        return self.min_node(self.root).key

    def min_node(self, node):
        if node.left is None:
            return node
        else:
            return self.min_node(node.left)

    def max(self):
        if self.is_empty():
            return None
        return self.max_node(self.root).key

    def max_node(self, node):
        if node.right is None:
            return node
        else:
            return self.max_node(node.right)

    def floor(self, key):
        x = self.floor_node(key, self.root)

        if x is None:
            return None
        else:
            return x.key

    def floor_node(self, key, node):
        if node is None:
            return None

        compare = cmp(key, node.key)
        if compare == 0:
            return node
        if compare < 0:
            return self.floor_node(key, node.left)

        t = self.floor_node(key, node.right)
        if not t is None:
            return t
        else:
            return node

    def ceil(self, key):
        x = self.ceil_node(key, self.root)

        if x is None:
            return None
        else:
            return x.key

    def ceil_node(self, key, node):
        if node is None:
            return None

        compare = cmp(key, node.key)
        if compare == 0:
            return node
        if compare > 0:
            return self.ceil_node(key, node.right)

        t = self.ceil_node(key, node.left)
        if not t is None:
            return t
        else:
            return node

    def select(self, k):
        """Return the key that is at rank k, 0-indexed."""
        if k < 0 or k >= self.size():
            return None

        x = self.select_node(k, self.root)
        return x.key

    def select_node(self, k, node):
        t = self.size_node(node.left)
        if t > k:
            return self.select_node(k, node.left)
        elif t < k:
            return self.select_node(k - t - 1, node.right)
        else:
            return node

    def rank(self, key):
        """The ordered position of the key, or number of keys less than
        key. 0-indexed.
        """
        return self.rank_node(key, self.root)

    def rank_node(self, key, node):
        if node is None:
            return 0

        compare = cmp(key, node.key)
        if compare < 0:
            return self.rank_node(key, node.left)
        elif compare > 0:
            return 1 + self.size_node(node.left) + \
                    self.rank_node(key, node.right)
        else:
            return self.size_node(node.left)

    # Range count and range search

    def keys(self):
        """Returns all of the keys."""
        return self.keys_between(self.min(), self.max())

    def keys_between(self, lo_key, hi_key):
        """Returns the keys between lo and hi"""
        queue = LinkedListQueue()
        self.keys_node(self.root, queue, lo_key, hi_key)
        return queue

    def keys_node(self, node, queue, lo_key, hi_key):
        if node is None:
            return

        compare_lo = cmp(lo_key, node.key)
        compare_hi = cmp(hi_key, node.key)

        if compare_lo < 0:
            self.keys_node(node.left, queue, lo_key, hi_key)
        if compare_lo <= 0 and compare_hi >= 0:
            queue.enqueue(node.key)
        if compare_hi > 0:
            self.keys_node(node.right, queue, lo_key, hi_key)

    # Testing functions
    def check_integrity(self):
        if not self.is_ordered(self.root, None, None):
            raise ValueError('BST is not in symmetric order!')
        if not self.is_23(self.root):
            raise ValueError('BST is not a 2-3 tree')
        if not self.is_balanced():
            raise ValueError('BST is not balanced!')
        return True

    def is_ordered(self, node, min_key, max_key):
        """Is the tree rooted at x a BST with all keys strictly between min and
        max (if min or max is null, treat as empty constraint)?
        """
        if node is None:
            return True

        if min_key is not None and cmp(node.key, min_key) <= 0:
            return False
        if max_key is not None and cmp(node.key, max_key) >= 0:
            return False

        return self.is_ordered(node.left, min_key, node.key) and \
                self.is_ordered(node.right, node.key, max_key)

    def is_23(self, node):
        """Does the tree have no red right links, and at most one (left)
        red links in a row on any path?
        """
        if node is None:
            return True

        if self.is_red(node.right):
            return False

        if node is not self.root and self.is_red(node) and \
           self.is_red(node.left):
            return False

        return self.is_23(node.left) and self.is_23(node.right)

    def is_balanced(self):
        """Do all paths from root to leaf have same number of black edges?"""
        black = 0
        node = self.root

        while node is not None:
            if not self.is_red(node):
                black += 1
            node = node.left

        return self.is_balanced_node(self.root, black)

    def is_balanced_node(self, node, black):
        if node is None:
            return black == 0

        if not self.is_red(node):
            black -= 1

        return self.is_balanced_node(node.left, black) and \
                self.is_balanced_node(node.right, black)

    # Magic method
    def __len__(self):
        return self.size()

    def __str__(self):
        return '%s: %d nodes' % (
            self.__class__.__name__, self.size()
        )
