import unittest
from Document import Document


class DocumentTest(unittest.TestCase):
    def setUp(self):
        self.d = Document()

    def test_len(self):
        self.assertEqual(0, len(self.d))
        self.d.add_row({'a': ['aaa']})
        self.assertEqual(1, len(self.d))
        self.d.add_row({'b': ['bbb']})
        self.assertEqual(2, len(self.d))

    def test_iter(self):
        self.assertEqual([], list(self.d))
        a = self.d.add_row({'a': ['aaa']})
        self.assertEqual([a], list(self.d))
        b = self.d.add_row({'b': ['bbb']})
        self.assertEqual([a, b], list(self.d))

    def test_getitem(self):
        self.assertRaises(IndexError, self.d.__getitem__, 0)
        a = self.d.add_row({'a': ['aaa']})
        self.assertEqual(a, self.d[0])
        self.assertRaises(IndexError, self.d.__getitem__, 1)
        b = self.d.add_row({'b': ['bbb']})
        self.assertEqual(a, self.d[0])
        self.assertEqual(b, self.d[1])
        self.assertRaises(IndexError, self.d.__getitem__, 2)

    def test_getitem_invalid(self):
        self.assertRaises(IndexError, self.d.__getitem__, -1)
        self.assertRaises(IndexError, self.d.__getitem__, 0)
        self.assertRaises(IndexError, self.d.__getitem__, 1000)
        self.d.add_row({'a': ['aaa']})
        self.assertRaises(IndexError, self.d.__getitem__, 1000)

    def test_remove(self):
        self.d.add_row({'a': ['aaa']})
        self.d[0].remove()

    def test_link(self):
        self.d.add_row({'a': ['a']})
        self.d.add_row({'a': ['aa']})
        self.d.add_row({'a': ['aaa']})
        d2 = Document()
        d2.add_row({'b': ['b']})
        d2.add_row({'b': ['bb']})
        joined = Document.join(self.d, d2)
        self.assertEqual(list(joined),
                         [
                             {'a': ['a'], 'b': ['b']},
                             {'a': ['aa'], 'b': ['bb']},
                             {'a': ['aaa']},
                         ])

    def test_split(self):
        row = self.d.add_row({
            'a': ['a', 'aa', 'aaa'],
            'b': ['b', 'bb', 'bbb'],
        })
        row.split({'a': 1, 'b': 2})
        self.assertEqual(list(self.d),
                         [
                             {'a': ['a'], 'b': ['b', 'bb']},
                             {'a': ['aa', 'aaa'], 'b': ['bbb']},
                         ])

    def test_merge(self):
        self.d.add_row({'a': ['a'], 'b': ['b']})
        self.d.add_row({'a': ['aa'], 'b': ['bb']})
        self.d[0].merge_next()
        self.assertEqual(list(self.d),
                         [{'a': ['a', 'aa'], 'b': ['b', 'bb']}])

    def test_align(self):
        row = self.d.add_row({
            'a': ['a', 'aa', 'aaa'],
            'b': ['b', 'bb', 'bbb'],
        })
        row.align()
        self.assertEqual(list(self.d),
                         [
                             {'a': ['a'], 'b': ['b']},
                             {'a': ['aa'], 'b': ['bb']},
                             {'a': ['aaa'], 'b': ['bbb']},
                         ])


class DocumentImportExportTest(unittest.TestCase):
    def setUp(self):
        self.d = Document()
        self.d.add_row({
            'a': ['a', 'aa', 'aaa'],
            'b': ['b', 'bb', 'bbb'],
        })
        self.d.add_row({
            'a': ['aaaa'],
            'c': ['c'],
        })
        self.d.add_row({
            'c': ['cc'],
        })

    def test_constructor(self):
        d2 = Document(self.d)
        self.assertEqual(list(self.d), list(d2))

    def test_json(self):
        d2 = Document.from_json(self.d.to_json())
        self.assertEqual(list(self.d), list(d2))


if __name__ == '__main__':
    unittest.main()