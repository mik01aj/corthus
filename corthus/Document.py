import itertools
import copy


class Document(object):
    def __init__(self, data=None):
        if not data:
            self._rows = []
        else:
            assert isinstance(data, Document)
            self._rows = copy.deepcopy(data._rows)

    def append(self, row_data):
        return self.insert(len(self._rows), row_data)

    def insert(self, index, row_data):
        """
        Insert a row before `index`.
        """
        assert 0 <= index <= len(self._rows)
        new_row = _Row(self, row_data)
        if index > 0:
            self._rows[index - 1]._next = new_row
            new_row._prev = self._rows[index - 1]
        if index < len(self._rows):
            self._rows[index]._prev = new_row
            new_row._next = self._rows[index]
        new_row._index = index
        self._rows.insert(index, new_row)
        for i in xrange(index, len(self._rows)): # this makes the whole operation O(n)
            self._rows[i]._index = i
        return new_row

    @classmethod
    def zip(cls, *documents):
        new_doc = Document()
        for row_dicts in itertools.izip_longest(*documents):
            new_row_data = {}
            for d in row_dicts:
                if d:
                    new_row_data.update(d)
            new_doc.append(new_row_data)
        return new_doc

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, n):
        r = self._rows[n]
        assert r._index == n
        return r

    def __iter__(self):
        return iter(self._rows)


class _Row(dict):
    def __init__(self, document, row_data, index=None, prev_row=None, next_row=None):
        dict.__init__(self, row_data)
        self.document = document
        self._prev = prev_row
        self._next = next_row
        self._index = index

    def remove(self):
        if self._prev:
            self._prev._next = self._next
        if self._next:
            self._next._prev = self._prev
        self.document._rows.remove(self)

    def add_before(self, new_row):
        self.document.insert(self._index, new_row)

    def add_after(self, new_row):
        self.document.insert(self._index + 1, new_row)

    def split(self, indices):
        assert self.keys() == indices.keys()
        new_row_data = dict()
        for key in self:
            new_row_data[key] = self[key][indices[key]:]
            self[key] = self[key][:indices[key]]
        self.add_after(new_row_data)

