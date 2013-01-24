#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script reads alignment files and collects all the found pairs. As
output, it prints all repeated pairs, starting from the most frequent.

Usage: ./alignment_analysis.py file1.pl-cu.hunalign [file2.pl-cu.golden...]
       (assuming existence of file1.pl.txt, file1.cu.txt, and so on)
or:    ./alignment_analysis.py `find texts/ -name '*.pl-cu.hunalign'`
"""

from __future__ import division

import sys
from toolkit import Text, Alignment
import re
from collections import defaultdict

from toolkit.preprocess import preprocess

lang1 = '' # a hack to get languages easily
lang2 = ''

def read_all_pairs(filename):
    """Iterates over sentence pairs in a file.
    """
    m = re.match('(.*)/(\w\w)-(\w\w).\w+$', filename)
    assert m
    basename = m.group(1)
    global lang1, lang2
    lang1 = m.group(2)
    lang2 = m.group(3)
    try:
        alignment = Alignment.from_file(filename)
    except ValueError:
        return
    t1 = Text.from_file(basename + '/' + lang1 + '.txt', lang1)
    t2 = Text.from_file(basename + '/' + lang2 + '.txt', lang2)
    seq1 = t1.as_sentences_flat()
    seq2 = t2.as_sentences_flat()
#    print "%s text: %d sentences" % (lang1, len(seq1))
#    print "%s text: %d sentences" % (lang2, len(seq2))
    separator = unicode(' ♦ ', 'utf-8')
    for s1, s2 in alignment.as_ranges(seq1, seq2):
        s1 = preprocess(separator.join(s1))
        s2 = preprocess(separator.join(s2))
        yield s1, s2

if __name__ == '__main__':

    # occurence counts for pairs and sentences
    occ_pairs = defaultdict(lambda: 0)
    occ_sent1 = defaultdict(lambda: 0)
    occ_sent2 = defaultdict(lambda: 0)

    filenames = sys.argv[1:]
    if not filenames:
        print __doc__
        sys.exit()

    for f in filenames:
        for s1, s2 in read_all_pairs(f):
            if s1 and s2:
                occ_sent1[s1] += 1
                occ_sent2[s2] += 1
                occ_pairs[s1, s2] += 1

    num_possible_pairs = ((len(occ_sent1) + 1) *
                          (len(occ_sent2) + 1)) # +1 for hapax pair
    hapax_prob = (1/num_possible_pairs) # same as normal, with count=occ*=0

    pairs_list = []
    for (s1, s2), pair_count in occ_pairs.iteritems():

        if pair_count < 2:
            continue

        occ1 = occ_sent1[s1]
        occ2 = occ_sent2[s2]

        # calculate_cost
        prob = (pair_count*2 + 1/num_possible_pairs) / (occ1 + occ2 + 1)
        assert prob > hapax_prob

        pairs_list.append((prob, s1, s2, pair_count, occ1, occ2))

    pairs_list.sort(reverse=True)

    print '_f', 'p', hapax_prob
    print

    for prob, s1, s2, pair_count, occ1, occ2 in pairs_list:
        print ("_f %d %s %d %s %d p %.4f" %
               (pair_count, lang1, occ1, lang2, occ2, prob))
        print lang1, s1.encode('utf-8')
        print lang2, s2.encode('utf-8')
        print
