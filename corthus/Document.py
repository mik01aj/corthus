import itertools


class Document(object):
    def __init__(self, data=None):
        if not data:
            self.first_row = None
            self.last_row = None
        self._length = 0

    class Row(dict):
        def __init__(self, document, row_data, prev_row=None, next_row=None):
            dict.__init__(self, row_data)
            self.document = document
            self.dict = dict
            self.prev_row = prev_row
            self.next_row = next_row

    def add_row(self, row_data):
        self._length += 1
        new_row = Document.Row(self, row_data, prev_row=self.last_row)
        if not self.first_row:
            self.first_row = self.last_row = new_row
        else:
            self.last_row.next_row = new_row
            self.last_row = new_row
        return new_row

    def __len__(self):
        return self._length

    def __getitem__(self, n):
        try:
            return next(itertools.islice(self, n, None))
        except (StopIteration, ValueError):
            raise IndexError(n)

    def __iter__(self):
        row = self.first_row
        while row:
            yield row
            row = row.next_row