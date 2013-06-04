from unittest import TestCase

from omnitool.datastructures.bst import RedBlackBST


class RedBlackBSTTest(TestCase):
    dict_alphabet = dict([(x, chr(x)) for x in range(65, 91)])

    def setUp(self):
        self.bst = RedBlackBST()
        self.assertEqual(self.bst.size(), 0)
        self.assertTrue(self.bst.is_empty())
        self.assertIs(self.bst.root, None)

    def _put_alphabet(self):
        """Adds capital letters and their ASCII codes as key to BST."""
        for k, v in self.dict_alphabet.iteritems():
            self.bst.put(k, v)

    def test_put_single_value(self):
        k = 1
        v = 'Test!'
        self.bst.put(k, v)
        self.assertEqual(self.bst.size(), 1)
        self.assertFalse(self.bst.is_empty())
        self.assertEqual(self.bst.root.key, k)
        self.assertEqual(self.bst.root.value, v)

    def test_get(self):
        k = 1337
        v = 'Test!'
        self.bst.put(k, v)
        res = self.bst.get(k)
        self.assertIsNot(res, None)
        self.assertEqual(res, v)
        self.assertIs(res, v)

    def test_len_magic_method(self):
        k = 1
        v = 'Test!'
        self.bst.put(k, v)
        self.assertEqual(len(self.bst), 1)

    def test_contains_key_starting_at_root(self):
        k = 1
        v = 'Test!'
        self.bst.put(k, v)
        self.assertTrue(self.bst.contains(k))
        self.assertFalse(self.bst.contains(k + 1))

    def test_symmetric_order(self):
        self._put_alphabet()
        self.assertEqual(self.bst.size(), 26)
        self.assertTrue(self.bst.is_ordered(self.bst.root, None, None))
        self.assertTrue(self.bst.is_ordered(self.bst.root, None, None))

    def test_is_23(self):
        self._put_alphabet()
        self.assertTrue(self.bst.is_23(self.bst.root))

    def test_is_balanced(self):
        self._put_alphabet()
        self.assertTrue(self.bst.is_balanced())

    def test_check_integrity(self):
        self._put_alphabet()
        self.assertTrue(self.bst.check_integrity())

    def test_delete(self):
        self._put_alphabet()
        org_size = self.bst.size()
        self.assertTrue(self.bst.contains(70))  # F
        self.bst.delete(70)
        self.assertFalse(self.bst.contains(70))
        self.assertEqual(self.bst.size(), org_size - 1)
        self.bst.delete(69)
        self.assertEqual(self.bst.size(), org_size - 2)

    def test_delete_min(self):
        self._put_alphabet()
        org_size = self.bst.size()
        self.assertTrue(self.bst.contains(65))  # A
        self.bst.delete_min()
        self.assertFalse(self.bst.contains(65))
        self.assertEqual(self.bst.size(), org_size - 1)

    def test_delete_max(self):
        self._put_alphabet()
        org_size = self.bst.size()
        self.assertTrue(self.bst.contains(90))
        self.bst.delete_max()
        self.assertFalse(self.bst.contains(90))
        self.assertEqual(self.bst.size(), org_size - 1)

    def test_rank(self):
        self._put_alphabet()
        self.assertEqual(self.bst.rank(66), 1)
        self.assertEqual(self.bst.rank(90), 25)

    def test_select(self):
        self._put_alphabet()
        self.assertEqual(self.bst.select(4), 69)  # E

    def test_keys(self):
        self._put_alphabet()
        result = self.bst.keys()
        self.assertEqual(len(result), 26)

    def test_keys_between(self):
        self._put_alphabet()
        expected = list(range(65, 71))
        result = self.bst.keys_between(65, 70)
        self.assertEqual(len(result), len(expected))

    def test_min(self):
        self._put_alphabet()
        self.assertEqual(self.bst.min(), 65)

    def test_max(self):
        self._put_alphabet()
        self.assertEqual(self.bst.max(), 90)

    def test_floor(self):
        self._put_alphabet()
        self.assertEqual(self.bst.floor(9001), 90)

    def test_floor_not_found(self):
        self._put_alphabet()
        self.assertEqual(self.bst.floor(1), None)

    def test_ceil(self):
        self._put_alphabet()
        self.assertEqual(self.bst.ceil(1), 65)

    def test_ceil_not_found(self):
        self._put_alphabet()
        self.assertEqual(self.bst.ceil(1337), None)
