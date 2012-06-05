
import codecs

"""
A class for managing large sets of translation pairs.
"""

#TODO sentence occurence count and pair occurence count

class PairManager:

    def __init__(self, pairs):
        """pairs: list of sentence pairs
        """
        self.pairs = set(pairs)
        self.forward = { a : b for (a, b) in pairs }
        self.reversed = { b : a for (a, b) in pairs }

    @classmethod
    def from_file(cls, file_path):
        pairs = set()
        with codecs.open(file_path, encoding='utf-8') as f:
            for (count, s1, s2, emptyline) in _group_by_4(f):
                pairs.add( (s1.strip(), s2.strip()) )
                #count = int(count)
                assert emptyline == '\n'
        return PairManager(pairs)

    def has_pair(self, s1, s2):
        return ((s1, s2) in self.pairs)

    def has_sent1(self, s):
        return s in self.forward

    def has_sent2(self, s):
        return s in self.reversed


def _group_by_4(iterator):
    while True:
        a = next(iterator) # StopIteration here is ok
        try:
            b = next(iterator)
            c = next(iterator)
            d = next(iterator)
            yield (a, b, c, d)
        except StopIteration:
            assert False, "sequence length should be divisible by 4"


# test (very simple, executed at each import)
_pm = PairManager([('a', 'b'), ('a', 'c')])
assert _pm.has_pair('a', 'c')
assert _pm.has_sent1('a')
assert _pm.has_sent2('b')
assert not _pm.has_sent2('a')
del _pm
