#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains the MultiAlignment class, which is used to handle
multi-language alignments.

You can also run this file from the command line to pretty-print an
alignment.
"""

from __future__ import unicode_literals

import csv

class MultiAlignment:

    """A class to hold an N-way alignment. It doesn't know anything
    about the texts. Only some methods, which need to access the text,
    have a *sequences parameter. This means, each of these methods
    expects N sequences (the original sequences, which were aligned).
    """

    def __init__(self, data, add_zeros=False):
        """Constructor.

        data: sequence of N-tuples: (index_1, index_2, ..., index_N, cost)

        If the first row does not contaion zeros, and the alignment
        starts at the beginning of sequence, you can add them with
        add_zeros=True. (needed with hunalign)
        """
        data = tuple(data)
        if not data:
            raise ValueError
        N = len(data[0]) - 1
        if N < 2:
            raise ValueError
        previous_row = [0 for i in range(N)]
        for row in data:
            if len(row) != N+1 or not all(row[i] >= previous_row[i] for i in range(N)):
                raise ValueError
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
                data.append([int(x) for x in row[:-1]] + [float(row[-1])])
        return MultiAlignment(data, *args, **kwargs)

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
            return data
        else:
            return tuple(row[:-1] for row in data)

    def as_ranges(self, *sequences, **kwargs):
        """sequences parameter is optional here
        """
        with_costs = kwargs.get('with_costs', False)
        def gen():
            previous_row = self.data[0]
            if len(sequences) != 0 and len(sequences) != self.N:
                raise ValueError
            for row in self.data[1:]:
                result_row = []
                if sequences:
                    for i in range(self.N):
                        if len(sequences[i]) <= row[i]:
                            raise IndexError("sequence too short", i, row[i], sequences[i])
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
        """Return precision and recall from comparison of two alignments.
        """
        intersection = set(row[:-1] for row in self.data) & \
                       set(row[:-1] for row in golden)
        precision = len(intersection) / len(self.data)
        recall = len(intersection) / len(golden)
        return "Precision: %.2f%%, Recall: %.2f%%" % (precision*100, recall*100)
        #return (precision, recall)

    def pretty_print(self, *sequences):
        from textwrap import wrap
        from itertools import izip_longest
        if len(sequences) != self.N:
            raise ValueError
        # ₀₁₂₃₄₅₆₇₈₉ ⁰¹²³⁴⁵⁶⁷⁸⁹ 𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡
        for row in list(self.as_ranges(with_costs=True)):
            lines = [] # will be a list of lists
            for i in range(self.N):
                lines.append([])
                _j, j = row[i]
                for s, num in zip(sequences[i][_j:j], range(_j, j)):
                    n = '♦' + unicode(num) + ' '
                    lines[-1].extend(wrap(n + s, 35))
            lines.append(["%.1f" % row[-1]]) # cost
            for output_row in izip_longest(*lines): # one output_row = one line of output
                output_row = list(output_row)
                for i in range(self.N+1):
                    if output_row[i] == None:
                        output_row[i] = ""
                s = "|".join("%-35s " % col for col in output_row[:-1])
                s += " |" + output_row[-1]
                print s.encode('utf-8') # a workaround for `less`
            print


if __name__ == '__main__':
    import sys
    import re
    from toolkit import Text

    [alignment_filename] = sys.argv[1:]

    m = re.match(r'(.*)\.(..)-(..)\.(.*)$', alignment_filename)
    a = MultiAlignment.from_file(alignment_filename)
    t1 = Text.from_file("%s.%s.txt" % (m.group(1), m.group(2)), lang=m.group(2))
    t2 = Text.from_file("%s.%s.txt" % (m.group(1), m.group(3)), lang=m.group(3))
    a.pretty_print(t1.as_sentences_flat(),
                   t2.as_sentences_flat())
    print "Total cost: " + str(sum(c for (_, _, c) in a.data))
