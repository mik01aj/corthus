#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains the Alignment class, which is used to handle
text alignments. You can also run this file from the command line
to pretty-print an alignment.
"""

import csv

class Alignment:

    """A class to hold an alignment. It doesn't know anything about the texts.
    """

    def __init__(self, data):
        """Constructor.
        data: sequence of 3-tuples: (index1, index2, cost)
        """
        data = tuple(data)
        if not data or not isinstance(data[0], tuple):
            raise ValueError
        _i, _j = 0, 0
        for i, j, c in data:
            assert _i <= i, (_i, i)
            assert _j <= j, (_j, j)
            _i, _j = i, j
        self.data = data

    @classmethod
    def from_file(cls, file_path, *args, **kwargs):
        with open(file_path) as f:
            return Alignment([(int(i), int(j), float(k))
                              for (i, j, k) in csv.reader(f, dialect='excel-tab')],
                             *args, **kwargs)

    def dump(self, file_path):
        with open(file_path, 'w') as f:
            writer = csv.writer(f, dialect='excel-tab')
            writer.writerows(self.data)

    def summed_cost(self):
        return sum(c for (i, j, c) in self.data)

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
                    yield s1, s2, _c
                else:
                    yield s1, s2
                _i, _j, _c = i, j, c
        return tuple(gen())

    def as_pairs(self, seq1=None, seq2=None, with_costs=False):
        """Iterate only over 1-1 matches. This means bisentences in a
        sentence-level alignment.
        """
        def gen():
            _i, _j, _c = 0, 0, 1
            for i, j, c in self.data:
                if (i, j) == (_i + 1, _j + 1):
                    s1 = seq1[_i] if seq1 else _i
                    s2 = seq2[_j] if seq2 else _j
                    if with_costs:
                        yield s1, s2, _c
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

    def pretty_print(self, seq1, seq2):
        from textwrap import wrap
        from itertools import izip_longest
        # ₀₁₂₃₄₅₆₇₈₉ ⁰¹²³⁴⁵⁶⁷⁸⁹ 𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡
        for (_i, i), (_j, j), c in list(self.as_ranges(with_costs=True)):
            ls1 = []
            for s, num in zip(seq1[_i:i], range(_i, i)):
                n = unicode('♦', 'utf-8') + str(num) + ' '
                ls1.extend(wrap(n + s, 35))
            ls2 = []
            for s, num in zip(seq2[_j:j], range(_j, j)):
                n = unicode('♦', 'utf-8') + str(num) + ' '
                ls2.extend(wrap(n + s, 35))
            for l1, l2, c in izip_longest(ls1, ls2, ["%.1f" % c]):
                l1 = l1 if l1 != None else ""
                l2 = l2 if l2 != None else ""
                c = c if c != None else ""
                s = unicode("%-35s │%-35s │%4s", 'utf-8') % (l1, l2, c)
                print s.encode('utf-8') # a workaround for `less`
            print ' '*79


if __name__ == '__main__':
    import sys
    import re
    from Text import Text

    [alignment_filename] = sys.argv[1:]

    m = re.match(r'(.*)\.(..)-(..)\.(.*)$', alignment_filename)
    a = Alignment.from_file(alignment_filename)
    t1 = Text.from_file("%s.%s.txt" % (m.group(1), m.group(2)), lang=m.group(2))
    t2 = Text.from_file("%s.%s.txt" % (m.group(1), m.group(3)), lang=m.group(3))
    a.pretty_print(t1.as_sentences_flat(),
                   t2.as_sentences_flat())
    print "Total cost: " + str(sum(c for (_, _, c) in a.data))

#    for ss1, ss2, c in list(a.as_ranges(t1.as_sentences_flat(), t2.as_sentences_flat(), with_costs=True)):
#        c /= 1+sum(len(s) for s in ss1) + sum(len(s) for s in ss2)
#        c *= 10
#        print "%3d %3d %30s|%s" % (len(ss1), len(ss2), '#'*-int(c), '#'*int(c))
