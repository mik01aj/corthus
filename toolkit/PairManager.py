# -*- coding: utf-8 -*-

from __future__ import division

import codecs
from collections import defaultdict

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

    @classmethod
    def from_corpus(cls, files_with_alignments, lang1, lang2):
        #XXX not tested
        d = defaultdict(lambda: defaultdict(lambda: 0))
        separator = unicode(' ♦ ', 'utf-8')
        for file1, file2, alignment_file in files_with_alignments:
            seq1 = Text.from_file(file1, lang1).as_sentences_flat()
            seq2 = Text.from_file(file2, lang2).as_sentences_flat()
            alignment = Alignment.from_file(alignment_file)
            for fragment1, fragment2 in alignment.as_ranges(seq1, seq2):
                fragment1 = separator.join(fragment1)
                fragment2 = separator.join(fragment2)
                d[fragment1][fragment2] += 1

    def has_pair(self, s1, s2):
        return ((s1, s2) in self.pairs)

    def has_sent(self, s):
        return s in self.forward

    def cond_prob(self, s1, s2):
        """This means P(s2 | s1), a probability that s1 was translated to s2.
        """
        pair_occurences = 0
        s1_occurences = 0
        if self.d.get(s1):
            s1_occurences = sum(l for (_, l) in self.d[s1].iteritems())
            if s2 in d[s1]:
                pair_occurences = self.d[s1][s2]
        # we're pretending that we saw the pair one more time
        return (pair_occurences + 1) / (s1_occurences + 1)


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
