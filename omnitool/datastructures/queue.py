"""Implementations of the queue datastructure.

Queues represent a first-in-first-out (FIFO) collection of items.
"""


class LinkedListQueue(object):
    """Queue, implemented using a linked list."""
    class Node(object):
        def __init__(self, item, next_node=None):
            self.item = item
            self.next_node = next_node

    def __init__(self):
        self.N = 0
        # Beginning of queue
        self.first = None
        # End of queue
        self.last = None

    def is_empty(self):
        """Is the queue empty?"""
        return self.first is None

    def size(self):
        """Return the number of items in the queue."""
        return self.N

    def peek(self):
        """Return the item least recently added to the queue. Does not modify
        the queue.
        """
        if self.is_empty():
            raise ValueError('Queue underflow')
        return self.first.item

    def enqueue(self, item):
        """Add an item to the queue."""
        old_last = self.last
        self.last = self.Node(item)

        if self.is_empty():
            self.first = self.last
        else:
            old_last.next_node = self.last

        self.N += 1

    def dequeue(self):
        """Remove and return the item on the queue least recently added (e.g.
        at the front.)
        """
        if self.is_empty():
            raise ValueError('Queue underflow')

        item = self.first.item
        self.first = self.first.next_node
        self.N -= 1

        if self.is_empty():
            self.last = None  # To avoid loitering

        return item

    def items(self):
        """Returns a list of items in the queue, starting with the item in the
        front of the queue.
        """
        current = self.first
        output = []

        while current is not None:
            output.append(current.item)
            current = current.next_node

        return output

    def iteritems(self):
        """Returns items in the queue as a generator, starting with the item in
        the front of the queue.
        """
        current = self.first

        while current is not None:
            yield current.item
            current = current.next_node

    # Magic methods
    def __iter__(self):
        return self.iteritems()

    def __len__(self):
        return self.size()

    def __str__(self):
        return 'Queue: [' + ', '.join(self.items()) + ']'
