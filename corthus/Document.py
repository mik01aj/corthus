import itertools


class Document(object):
    def __init__(self, data=None):
        if not data:
            self._rows = []
        self._length = 0

    class _Row(dict):
        def __init__(self, document, row_data, prev_row=None, next_row=None):
            dict.__init__(self, row_data)
            self.document = document
            self.dict = dict
            self._prev = prev_row
            self._next = next_row

        def remove(self):
            if self._prev:
                self._prev._next = self._next
            if self._next:
                self._next._prev = self._prev
            self.document._rows.remove(self)

    def add_row(self, row_data):
        self._length += 1
        new_row = Document._Row(self, row_data)
        if self._rows:
            self._rows[-1]._next = new_row
            new_row._prev = self._rows[-1]
        self._rows.append(new_row)
        return new_row

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, n):
        return self._rows[n]

    def __iter__(self):
        return iter(self._rows)
