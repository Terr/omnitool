

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
    def delete_min(self, node=None):
        if self.is_empty():
            raise ValueError('BST underflow')

        # If both children of root are black, set root to red
        if not self.is_red(self.root.left) and \
           not self.is_red(self.root.right):
            self.root.color = self.RED

        if node is None:
            self.root = self.delete_min(self.root)
        else:
            if node.left is None:
                return None

            if not self.is_red(node.left) and \
               not self.is_red(node.left.left):
                node = self.move_red_left(node)

            node.left = self.delete_min(node.left)

            return self.balance(node)

        if not self.is_empty():
            self.root.color = self.BLACK

    # Delete the key-value pair with the maximum key rooted at node
    def delete_max(self, node=None):
        if self.is_empty():
            raise ValueError('BST underflow')

        # If both children of root are black, set root to red
        if not self.is_red(self.root.left) and \
           not self.is_red(self.root.right):
            self.root.color = self.RED

        if node is None:
            self.root = self.delete_max(self.root)
        else:
            if self.is_red(node.left):
                node = self.rotate_right(node)

            if node.right is None:
                return None

            if not self.is_red(node.right) and \
               not self.is_red(node.right.left):
                node = self.move_red_right(node)

            node.right = self.delete_max(node.right)

            return self.balance(node)

        if not self.is_empty():
            self.root.color = self.BLACK

    def delete(self, key, node=None):
        if not self.contains(key):
            raise ValueError('Tree does not contain key %s' % key)

        # If both children of root are black, set root to red
        if not self.is_red(self.root.left) and \
           not self.is_red(self.root.right):
            self.root.color = self.RED

        if node is None:
            self.root = self.delete(key, self.root)
        else:
            if cmp(key, node.key) < 0:
                if not self.is_red(node.left) and \
                   not self.is_red(node.left.left):
                    node = self.move_red_left(node)

                node.left = self.delete(key, node.left)
            else:
                if self.is_red(node.left):
                    node = self.rotate_right(node)

                if cmp(key, node.key) == 0 and node.right is None:
                    return None

                if not self.is_red(node.right) and \
                   not self.is_red(node.right.left):
                    node = self.move_red_right(node)

                if cmp(key, node.key) == 0:
                    node.value = self.get_node(self.min(node.right).key, node.right)
                    node.key = self.min(node.right).key
                    node.right = self.delete_min(node.right)
                else:
                    node.right = self.delete(key, node.right)

            return self.balance(node)

        if not self.is_empty():
            self.root.color = self.BLACK

    #
    # Red-Black tree helper functions
    #

    # Make a left-leaning link lean to the right
    def rotate_right(self, node):
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
        node.color = not node.color
        node.left.color = not node.left.color
        node.right.color = not node.right.color

    # Assuming that h is red and both h.left and h.left.left
    # are black, make h. or one of its children red.
    def move_red_left(self, node):
        self.flip_colors(node)
        if self.is_red(node.right.left):
            node.right = self.rotate_right(node.right)
            node = self.rotate_left(node)

        return node

    # Assuming that h is red and both h.right and h.right.left
    # are black, make h.right or one of its children red.
    def move_red_right(self, node):
        self.flip_colors(node)
        if self.is_red(node.left.left):
            node.right = self.rotate_right(node)

        return node

    # Restore red-black tree invariant
    def balance(self, node):
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
        return self.min_ndoe(self.root).key

    def min_node(self, node):
        if node.left is None:
            return node
        else:
            return self.min_node(node.left)

    def max(self):
        if self.is_empty():
            return None
        return self.max(self.root).key

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

    def ceiling(self, key):
        x = self.ceiling_node(key, self.root)

        if x is None:
            return None
        else:
            return x.key

    def ceiling_node(self, key, node):
        if node is None:
            return None

        compare = cmp(key, node.key)
        if compare == 0:
            return node
        if compare > 0:
            return self.ceiling_node(key, node.right)

        t = self.ceiling_node(key, node.left)
        if not t is None:
            return t
        else:
            return node

    # The key of rank k
    def select(self, k):
        if k < 0 or k >= self.size():
            return None

        x = self.select_node(k, self.root)
        return x.key

    def select_node(self, k, node):
        t = self.size_node(node.left)
        if t > k:
            return self.select(k, node.left)
        elif t < k:
            return self.select(k - t - 1, node.right)
        else:
            return node

    # Number of keys less than key
    def rank(self, key):
        return self.rank_node(key, self.root)

    def rank_node(self, key, node):
        if node is None:
            return 0

        compare = cmp(key, node.key)
        if cmp < 0:
            return self.rank_node(key, node.left)
        elif cmp > 0:
            return 1 + self.size_node(node.left) + \
                    self.rank_node(key, node.right)
        else:
            return self.size_node(node.left)


    #
    # Ordered symbol table methods
    #
    def min(self, node=None):
        if self.is_empty():
            return None

        if node is None:
            return self.min(self.root).key
        else:
            if node.left is None:
                return node
            else:
                return self.min(node.left)

    def max(self, node=None):
        if self.is_empty():
            return None

        if node is None:
            return self.max(self.root).key
        else:
            if node.right is None:
                return node
            else:
                return self.max(node.right)

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

    def ceiling(self, key):
        x = self.ceiling_node(key, self.root)

        if x is None:
            return None
        else:
            return x.key

    def ceiling_node(self, key, node):
        if node is None:
            return None

        compare = cmp(key, node.key)
        if compare == 0:
            return node
        if compare > 0:
            return self.ceiling_node(key, node.right)

        t = self.ceiling_node(key, node.left)
        if not t is None:
            return t
        else:
            return node

    # The key of rank k
    def select(self, k):
        if k < 0 or k >= self.size():
            return None

        x = self.select_node(k, self.root)
        return x.key

    def select_node(self, k, node):
        t = self.size_node(node.left)
        if t > k:
            return self.select(k, node.left)
        elif t < k:
            return self.select(k - t - 1, node.right)
        else:
            return node

    # Number of keys less than key
    def rank(self, key):
        return self.rank_node(key, self.root)

    def rank_node(self, key, node):
        if node is None:
            return 0

        compare = cmp(key, node.key)
        if cmp < 0:
            return self.rank_node(key, node.left)
        elif cmp > 0:
            return 1 + self.size_node(node.left) + \
                    self.rank_node(key, node.right)
        else:
            return self.size_node(node.left)

    # Range count and range search

    def keys(self):
        """Returns all of the keys."""
        return self.keys_between(self.min(), self.max())

    def keys_between(self, lo, hi):


if __name__ == '__main__':
    bst = RedBlackBST()
    bst.put('A', 1)
    bst.put('B', 1)
    bst.put('C', 1)
    bst.put('E', 1)
    import debug
