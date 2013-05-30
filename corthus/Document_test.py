import unittest
from Document import Document


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.d = Document()

    def test_len(self):
        self.assertEqual(0, len(self.d))
        self.d.add_row({'a': 'aaa'})
        self.assertEqual(1, len(self.d))
        self.d.add_row({'b': 'bbb'})
        self.assertEqual(2, len(self.d))

    def test_iter(self):
        self.assertEqual([], list(self.d))
        a = self.d.add_row({'a': 'aaa'})
        self.assertEqual([a], list(self.d))
        b = self.d.add_row({'b': 'bbb'})
        self.assertEqual([a, b], list(self.d))

    def test_getitem(self):
        self.assertRaises(IndexError, self.d.__getitem__, 0)
        a = self.d.add_row({'a': 'aaa'})
        self.assertEqual(a, self.d[0])
        self.assertRaises(IndexError, self.d.__getitem__, 1)
        b = self.d.add_row({'b': 'bbb'})
        self.assertEqual(a, self.d[0])
        self.assertEqual(b, self.d[1])
        self.assertRaises(IndexError, self.d.__getitem__, 2)

    def test_getitem_invalid(self):
        self.assertRaises(IndexError, self.d.__getitem__, -1)
        self.assertRaises(IndexError, self.d.__getitem__, 1000)
        self.d.add_row({'a': 'aaa'})
        self.assertRaises(IndexError, self.d.__getitem__, -1)
        self.assertRaises(IndexError, self.d.__getitem__, 1000)


if __name__ == '__main__':
    unittest.main()