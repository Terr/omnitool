from unittest import TestCase

from datastructures.queue import LinkedListQueue


class LinkedListQueueTest(TestCase):
    def setUp(self):
        self.queue = LinkedListQueue()

    def test_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)

    def test_enqueue_single_item(self):
        s = 'Test!'
        self.queue.enqueue(s)
        self.assertFalse(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 1)
        self.assertEqual(self.queue.first, self.queue.last)

    def test_dequeue_single_item(self):
        s = 'Test!'
        self.queue.enqueue(s)
        self.queue.dequeue()
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)

    def test_peek(self):
        s = 'Test!'
        self.queue.enqueue(s)
        self.assertEqual(self.queue.size(), 1)
        self.assertEqual(self.queue.peek(), s)
        self.assertEqual(self.queue.size(), 1)

    def test_multiple_item_enqueue(self):
        s1 = 'Test 1!'
        s2 = 'Test 2!'
        self.queue.enqueue(s1)
        self.queue.enqueue(s2)
        self.assertEqual(self.queue.size(), 2)

    def test_multiple_item_dequeue_order(self):
        s1 = 'Test 1!'
        s2 = 'Test 2!'
        self.queue.enqueue(s1)
        self.queue.enqueue(s2)

        r1 = self.queue.dequeue()
        self.assertEqual(r1, s1)
        self.assertIs(r1, s1)

        r2 = self.queue.dequeue()
        self.assertEqual(r2, s2)
        self.assertIs(r2, s2)

        self.assertTrue(self.queue.is_empty())

    def test_get_items_list(self):
        s1 = 'Test 1!'
        s2 = 'Test 2!'
        self.queue.enqueue(s1)
        self.queue.enqueue(s2)

        l = self.queue.items()
        self.assertEqual(len(l), 2)
        self.assertEqual(l, [s1, s2])

    def test_to_string(self):
        s1 = 'Test 1!'
        s2 = 'Test 2!'
        self.queue.enqueue(s1)
        self.queue.enqueue(s2)
        self.assertEqual(
            str(self.queue),
            'Queue: [Test 1!, Test 2!]'
        )
