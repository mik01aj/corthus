import unittest
from Document import Document


class DocumentTest(unittest.TestCase):
    def setUp(self):
        self.d = Document()

    def test_len(self):
        self.assertEqual(0, len(self.d))
        self.d.append({'a': ['aaa']})
        self.assertEqual(1, len(self.d))
        self.d.append({'b': ['bbb']})
        self.assertEqual(2, len(self.d))

    def test_iter(self):
        self.assertEqual([], list(self.d))
        a = self.d.append({'a': ['aaa']})
        self.assertEqual([a], list(self.d))
        b = self.d.append({'b': ['bbb']})
        self.assertEqual([a, b], list(self.d))

    def test_getitem(self):
        self.assertRaises(IndexError, self.d.__getitem__, 0)
        a = self.d.append({'a': ['aaa']})
        self.assertEqual(a, self.d[0])
        self.assertRaises(IndexError, self.d.__getitem__, 1)
        b = self.d.append({'b': ['bbb']})
        self.assertEqual(a, self.d[0])
        self.assertEqual(b, self.d[1])
        self.assertRaises(IndexError, self.d.__getitem__, 2)

    def test_getitem_invalid(self):
        self.assertRaises(IndexError, self.d.__getitem__, -1)
        self.assertRaises(IndexError, self.d.__getitem__, 0)
        self.assertRaises(IndexError, self.d.__getitem__, 1000)
        self.d.append({'a': ['aaa']})
        self.assertRaises(IndexError, self.d.__getitem__, 1000)

    def test_remove(self):
        self.d.append({'a': ['aaa']})
        self.d[0].remove()

    def test_zip(self):
        self.d.append({'a': ['a']})
        self.d.append({'a': ['aa']})
        self.d.append({'a': ['aaa']})
        d2 = Document()
        d2.append({'b': ['b']})
        d2.append({'b': ['bb']})
        joined = Document.zip(self.d, d2)
        self.assertEqual(list(joined),
                         [
                             {'a': ['a'], 'b': ['b']},
                             {'a': ['aa'], 'b': ['bb']},
                             {'a': ['aaa']},
                         ])

    def test_split(self):
        row = self.d.append({
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
        self.d.append({'a': ['a'], 'b': ['b']})
        self.d.append({'a': ['aa'], 'b': ['bb']})
        self.d[0].merge_next()
        self.assertEqual(list(self.d),
                         [{'a': ['a', 'aa'], 'b': ['b', 'bb']}])

    def test_align(self):
        row = self.d.append({
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
        self.d.append({
            'a': ['a', 'aa', 'aaa'],
            'b': ['b', 'bb', 'bbb'],
        })
        self.d.append({
            'a': ['aaaa'],
            'c': ['c'],
        })
        self.d.append({
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