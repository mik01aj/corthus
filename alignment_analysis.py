#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script reads alignment files and collects all the found pairs. As
output, it prints all repeated pairs, starting from the most frequent.

Usage: ./alignment_analysis.py file1.pl-cu.hunalign [file2.pl-cu.golden...]
       (assuming existence of file1.pl.txt, file1.cu.txt, and so on)
or:    ./alignment_analysis.py `find texts/ -name '*.pl-cu.hunalign'`
"""

import sys
from toolkit import Text, Alignment
import re
from collections import defaultdict

all1 = []
all2 = []

def read_all_pairs(filename):
    """Iterates over sentence pairs in a file.
    (and adds all sentences to all1 and all2)
    """
    m = re.match('(.*)/(\w\w)-(\w\w).\w+$', filename)
    assert m
    basename = m.group(1)
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
        s1 = separator.join(s1)
        s2 = separator.join(s2)
        all1.append(s1)
        all2.append(s2)
        yield s1, s2

if __name__ == '__main__':

    # translation pair histogram
    translations = defaultdict(lambda: 0)
    sentence_occurences1 = defaultdict(lambda: 0)
    sentence_occurences2 = defaultdict(lambda: 0)

    filenames = sys.argv[1:]
    if not filenames:
        print __doc__
        sys.exit()

    for f in filenames:
        for s1, s2 in read_all_pairs(f):
            if s1 and s2:
                sentence_occurences1[s1] += 1
                sentence_occurences2[s2] += 1
                translations[s1, s2] += 1

    translations_as_list = [(count, translation)
                          for (translation, count)
                          in translations.iteritems()]
    translations_as_list.sort(reverse=True)

    freqs1 = defaultdict(lambda: 0)
    for sent in all1:
        freqs1[sent] += 1
    freqs2 = defaultdict(lambda: 0)
    for sent in all2:
        freqs2[sent] += 1

    for count, (s1, s2) in translations_as_list:
        if count < 2:
            break

        # if these sentences occur paired with each other,
        # at least every 5th time they occur at all
        if sentence_occurences1[s1] + sentence_occurences2[s2] > 10 * count:
            continue

        print count
        print freqs1[s1], s1.encode('utf-8')
        print freqs2[s2], s2.encode('utf-8')
        print
