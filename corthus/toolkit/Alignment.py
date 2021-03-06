#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains the Alignment class, which is used to handle
multi-language (2 or more) alignments.

You can also run this file from the command line to pretty-print an
alignment.

Usage examples:
    ./Alignment.py alignment.pl-cu.hunalign
         (the script will find the txt files)
    ./Alignment.py alignment.pl-cu.hunalign a.sentences b.sentences
         (the script will use given files as sentence files)
"""

from __future__ import unicode_literals
from __future__ import division

import csv

class Alignment:

    """A class to hold an N-way alignment. It doesn't know anything
    about the texts. Only some methods, which need to access the text,
    have a *sequences parameter. This means, each of these methods
    expects N sequences (the original sequences, which were aligned).
    """

    def __init__(self, data, add_zeros=False, no_costs=False):
        """Constructor.

        data: sequence of N-tuples: (index_1, index_2, ..., index_N, cost)

        If the first row does not contaion zeros, and the alignment
        starts at the beginning of sequence, you can add them with
        add_zeros=True. (needed with hunalign)

        If your data doesn't contain costs, use no_costs=True option.
        """
        data = list(data)
        assert data
        if no_costs:
            for i in xrange(len(data)):
                data[i] = tuple(data[i]) + (0, )
        N = len(data[0]) - 1
        assert data[0][-1]*0 + 1
        previous_row = [0 for i in range(N)]
        for row in data:
            assert len(row) == N+1
            assert all(row[i] >= previous_row[i] for i in range(N)), \
                (previous_row, row)
            previous_row = row
        if add_zeros:
            data = (tuple(0 for i in range(N+1)), ) + data # first cost=0
        self.data = data
        self.N = N

    @classmethod
    def from_file(cls, file_path, *args, **kwargs):
        data = []
        with open(file_path) as f:
            for row in csv.reader(f, dialect='excel-tab'):
                if kwargs.get('no_costs', False):
                    data.append([int(x) for x in row])
                else:
                    data.append([int(x) for x in row[:-1]] + [float(row[-1])])
        if not data:
            raise IOError, data
        return Alignment(data, *args, **kwargs)

    @classmethod
    def create_straight(cls, rows, cols):
        return Alignment([(i,) * cols for i in range(rows)],
                         no_costs=True)

    def dump(self, file_path):
        with open(file_path, 'w') as f:
            writer = csv.writer(f, dialect='excel-tab')
            writer.writerows(self.data)

    def summed_cost(self):
        return sum(row[-1] for row in self.data)

    def as_ladder(self, with_costs=False):
        """Iterates over rungs of the alignment (like in Hunalign's output)
        """
        if with_costs:
            return self.data
        else:
            return tuple(row[:-1] for row in self.data)

    def as_ranges(self, *sequences, **kwargs):
        """sequences parameter is optional here
        """
        with_costs = kwargs.get('with_costs', False)
        assert all(k in ['with_costs'] for k in kwargs)
        def gen():
            previous_row = self.data[0]
            if len(sequences) != 0 and len(sequences) != self.N:
                raise ValueError
            for row in self.data[1:]:
                result_row = []
                if sequences:
                    for i in range(self.N):
#                        if len(sequences[i]) <= row[i]:
#                            raise IndexError("sequence too short", i, row[i])
                        result_row.append(sequences[i][previous_row[i]:row[i]])
                else:
                    result_row = [(previous_row[i], row[i]) for i in range(self.N)]
                if with_costs:
                    result_row.append(previous_row[-1]) #XXX cost shifted one row
                yield result_row
                previous_row = row
        return list(gen())

    def as_pairs(self, *sequences, **kwargs):
        """Iterate only over 1-1 matches. This means bisentences in a
        sentence-level alignment. Sequences parameter is optional.
        """
        def gen():
            if sequences:
                for range_row in self.as_ranges(sequences, **kwargs):
                    if all(len(range_row[i]) == 1 for i in range(self.N)):
                        yield range_row
            else:
                range_rows = self.as_ranges(sequences, **kwargs)
                previous_row = range_rows[0]
                for range_row in range_rows[1:]:
                    if all(range_row[i] - previous_row[i] == 1 for i in range(self.N)):
                        yield range_row
                    previous_row = range_row
        return list(gen())

    def evaluate(self, golden):
        assert self.N == 2

        def as_pairs(a):
            for (s1, e1), (s2, e2) in a.as_ranges():
                i_s = range(s1, e1)
                if not i_s:
                    i_s = [None]
                j_s = range(s2, e2)
                if not j_s:
                    j_s = [None]
                weight = 1/(len(i_s)*len(j_s))
                for i in i_s:
                    for j in j_s:
                        yield (i, j), weight

        ps1 = dict(as_pairs(self))
        ps2 = dict(as_pairs(golden))

        assert abs(sum(ps1.values()) + 1 - len(self.data)) < 0.0001
        assert abs(sum(ps2.values()) + 1 - len(golden.data)) < 0.0001

        intersection_weight1 = sum(ps1[p] for p in set(ps1).intersection(ps2))
        intersection_weight2 = sum(ps2[p] for p in set(ps1).intersection(ps2))

        precision = intersection_weight1 / (len(self.data) - 1)
        recall    = intersection_weight2 / (len(golden.data) - 1)
        print "Precision: %.2f%%, Recall: %.2f%%" % (precision*100, recall*100)
        return (precision, recall)


    def pretty_print(self, *sequences):
        from textwrap import wrap
        from itertools import izip_longest
        if len(sequences) != self.N:
            raise ValueError, (len(sequences), self.N)
        # ₀₁₂₃₄₅₆₇₈₉ ⁰¹²³⁴⁵⁶⁷⁸⁹ 𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡
        for row in list(self.as_ranges(with_costs=True)):
            lines = [] # will be a list of lists
            for i in range(self.N):
                lines.append([])
                _j, j = row[i]
                for s, num in zip(sequences[i][_j:j], range(_j, j)):
                    n = '♦' + unicode(num) + ' '
                    lines[-1].extend(wrap(n + s, 35))
            lines.append(["%4.1f" % row[-1]]) # cost
            for output_row in izip_longest(*lines): # one output_row = one line of output
                output_row = list(output_row)
                for i in range(self.N+1):
                    if output_row[i] == None:
                        output_row[i] = ""
                s = "|".join("%-35s%s " % (col, ' '*col.count('\u0331'))
                             for col in output_row[:-1])
                s += " |" + output_row[-1]
                print s.encode('utf-8') # a workaround for `less`
            print


#if __name__ == '__main__':
#    a1 = Alignment.from_file('/tmp/pl-cu.my')
#    a2 = Alignment.from_file('/tmp/pl-cu.new')
#    a1.evaluate(a2)
#    a2.evaluate(a2)
#
#    half = Alignment(a2.data[:int(len(a2.data)/2)])
#    a2.evaluate(half)
#    half.evaluate(a2)
#
#    trivial = Alignment([a2.data[0], a2.data[-1]])
#    a2.evaluate(trivial)
#    trivial.evaluate(a2)
#
#    skip_all = Alignment([a2.data[0],
#                          (a2.data[0][0], a2.data[-1][1], 0),
#                          a2.data[-1]])
#    a2.evaluate(skip_all)
#    skip_all.evaluate(a2)
#
#
#    raise SystemExit

if __name__ == '__main__':
    import sys
    import re
    from Text import Text

    try:
        alignment_filename = sys.argv[1]
        if sys.argv[2:]:
            [fn1, fn2] = sys.argv[2:]
            assert not fn1.endswith('.txt')
            assert not fn2.endswith('.txt')
            with open(fn1) as f:
                seq1 = [l.decode('utf-8').strip() for l in f.readlines()]
                with open(fn2) as f:
                    seq2 = [l.decode('utf-8').strip() for l in f.readlines()]
        else:
            m = re.match(r'(.*/)?(..)-(..)\.(.*)$', alignment_filename)
            t1 = Text.from_file("%s%s.txt" % (m.group(1), m.group(2)),
                                lang=m.group(2))
            t2 = Text.from_file("%s%s.txt" % (m.group(1), m.group(3)),
                                lang=m.group(3))
            seq1 = t1.as_sentences_flat()
            seq2 = t2.as_sentences_flat()
        a = Alignment.from_file(alignment_filename)
        a.pretty_print(seq1, seq2)
        print "Total cost: " + str(sum(c for (_, _, c) in a.data))
    except IndexError, ValueError:
        print >> sys.stderr, __doc__
    except IOError, e:
        print >> sys.stderr, e
