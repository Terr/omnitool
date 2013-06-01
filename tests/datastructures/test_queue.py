from unittest import TestCase

from datastructures.queue import LinkedListQueue


class LinkedListQueueTest(TestCase):
    def setUp(self):
        self.queue = LinkedListQueue()
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
        self.assertIs(self.queue.peek(), s)
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
        s3 = 'Test 3!'
        self.queue.enqueue(s1)
        self.queue.enqueue(s2)
        self.queue.enqueue(s3)

        self.assertEqual(self.queue.first.item, s1)
        self.assertIs(self.queue.first.item, s1)
        self.assertEqual(self.queue.last.item, s3)
        self.assertIs(self.queue.last.item, s3)

        r1 = self.queue.dequeue()
        self.assertEqual(r1, s1)
        self.assertIs(r1, s1)
        self.assertEqual(self.queue.first.item, s2)
        self.assertIs(self.queue.first.item, s2)
        self.assertEqual(self.queue.last.item, s3)
        self.assertIs(self.queue.last.item, s3)

        r2 = self.queue.dequeue()
        self.assertEqual(r2, s2)
        self.assertIs(r2, s2)
        self.assertEqual(self.queue.first.item, s3)
        self.assertIs(self.queue.first.item, s3)
        self.assertIs(self.queue.first, self.queue.last)

        r3 = self.queue.dequeue()
        self.assertEqual(r3, s3)
        self.assertIs(r3, s3)

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

    def test_magic_len(self):
        s1 = 'Test 1!'
        s2 = 'Test 2!'
        self.queue.enqueue(s1)
        self.queue.enqueue(s2)
        self.assertEqual(len(self.queue), 2)

    def test_iteration_via_iteritems(self):
        values = ['Test 1!', 'Test 2!']
        for v in values:
            self.queue.enqueue(v)

        x = 0
        for i in self.queue.iteritems():
            self.assertIs(i, values[x])
            x += 1

    def test_iteration_via_magic_method(self):
        values = ['Test 1!', 'Test 2!']
        for v in values:
            self.queue.enqueue(v)

        x = 0
        for i in self.queue:
            self.assertIs(i, values[x])
            x += 1
