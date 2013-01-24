#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A class for managing large sets of translation pairs.
"""

from __future__ import unicode_literals

import codecs
import re

from NewAlignment import NewAlignment

class PairManager:

    def __init__(self):
        self.pairs = {}
        self.pairs_by_prob = []
        self.hapax_prob = None

    @classmethod
    def from_file(cls, file_path):
        m = re.match('.*(\w\w)-(\w\w)$', file_path)
        lang1 = m.group(1)
        lang2 = m.group(2)
        pm = PairManager()
        with codecs.open(file_path) as f:
            na = NewAlignment.read(f)
            first = True
            for row in na:
                if first:
                    pm.hapax_prob = float(row['_f'].split()[-1])
                    first = False
                    continue
                count = int(row['_f'].split()[0])
                prob = float(row['_f'].split()[-1])
                pm.pairs[row[lang1], row[lang2]] = (count, prob)
                pm.pairs_by_prob.append((prob, row[lang1], row[lang2]))
        pm.pairs_by_prob.sort(reverse=True)
        return pm

    def iter_best_pairs(self, threshold=None, count=None):
        """Iterate over `count` best pairs. If there are more than
        `count` with probability estimated above `threshold`, it will
        yield more."""
        for i, (prob, s1, s2) in enumerate(self.pairs_by_prob):
            if threshold and prob < threshold:
                if not count or i > count:
                    break
            yield prob, s1, s2

    def get_pair_prob(self, s1, s2):
        try:
            return self.pairs[s1, s2][1]
        except KeyError:
            return self.hapax_prob

    def has_pair(self, s1, s2):
        return (s1, s2) in self.pairs


if __name__ == '__main__':
    import matplotlib
#    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

#    size = 20
#    fig = plt.figure(figsize=(size, size))
    fig = plt.figure()
    ax = fig.add_subplot(111)

    pms = [PairManager.from_file('data/pairs.pl-cu'),
           PairManager.from_file('data/pairs.cu-el'),
           PairManager.from_file('data/pairs.pl-el')]

    styles = ['D', 'o', 's']

    for pm, st in zip(pms, styles):
        histogram = { i : 0 for i in range(100) }
        for count, _ in pm.pairs.itervalues():
            try:
                histogram[count] += 1
            except KeyError:
                histogram[count] = 1
        xs, ys = zip(*histogram.items())
        ax.plot(xs, ys, c=(0, 0, 0, 1))
    ax.set_xlabel(r'liczba wystąpień pary', fontsize=20)
    ax.set_ylabel(r'liczba par', fontsize=20)
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])
    ax.grid(True)

    plt.show()
