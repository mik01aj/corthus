
import csv

class Alignment:

    def __init__(self, data):
        """Constructor.
        data: list of 3-tuples: (index1, index2, cost)
        """
        data = tuple(data)
        assert isinstance(data[0], tuple)
        assert len(data[0]) == 3
        self.data = data

    @classmethod
    def from_file(cls, file_path, *args, **kwargs):
        with open(file_path) as f:
            return Alignment([(int(i), int(j), float(k))
                              for (i, j, k) in csv.reader(f)],
                             *args, **kwargs)

    def dump(self, file_path):
        with open(file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.data)

    def as_ladder(self, with_costs=False):
        def gen():
            for i, j, c in self.data:
                if with_costs:
                    yield i, j, c
                else:
                    yield i, j
        return tuple(gen())

    def as_ranges(self, seq1=None, seq2=None, with_costs=False):
        def gen():
            _i, _j, _c = 0, 0, 1
            for i, j, c in self.data:
                s1 = seq1[_i:i] if seq1 else (_i, i)
                s2 = seq2[_j:j] if seq2 else (_j, j)
                if with_costs:
                    yield s1, s2, c
                else:
                    yield s1, s2
                _i, _j, _c = i, j, c
        return tuple(gen())

    def as_pairs(self, seq1=None, seq2=None, with_costs=False):
        """Iterate only over 1-1 matches. (This means bisentences in a
        sentence-level alignment)
        """
        def gen():
            _i, _j, _c = 0, 0, 1
            for i, j, c in self.data:
                if (i, j) == (_i + 1, _j + 1):
                    print i, j, len(seq1), len(seq2) # XXX
                    s1 = seq1[_i] if seq1 else _i
                    s2 = seq2[_j] if seq2 else _j
                    if with_costs:
                        yield s1, s2, c
                    else:
                        yield s1, s2
                _i, _j, _c = i, j, c
        return tuple(gen())

    def evaluate(self, golden):
        intersection = set((i, j) for (i, j, c) in self.data) & \
                       set((i, j) for (i, j, c) in golden)
        precision = len(intersection) / len(self.data)
        recall = len(intersection) / len(golden)
        return "Precision: %.2f%%, Recall: %.2f%%" % (precision*100, recall*100)
        #return (precision, recall)

