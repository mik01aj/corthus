#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from toolkit import Text, Alignment
import re
from collections import defaultdict

def read_all_pairs(filename):
    """Iterates over sentence pairs in a file.
    """
    m = re.match('(.*)\.(\w\w)-(\w\w).\w+$', filename)
    assert m
    basename = m.group(1)
    lang1 = m.group(2)
    lang2 = m.group(3)
    alignment = Alignment.from_file(filename)
    t1 = Text.from_file(basename + '.' + lang1 + '.txt', lang1)
    t2 = Text.from_file(basename + '.' + lang2 + '.txt', lang2)
    seq1 = t1.as_sentences_flat()
    seq2 = t2.as_sentences_flat()
#    print "%s text: %d sentences" % (lang1, len(seq1))
#    print "%s text: %d sentences" % (lang2, len(seq2))
    separator = unicode(' ♦ ', 'utf-8')
    for s1, s2 in alignment.as_ranges(seq1, seq2):
        yield separator.join(s1), separator.join(s2)

if __name__ == '__main__':

    # translation pair histogram
    translations = defaultdict(lambda: 0)

    filenames = sys.argv[1:]
    for f in filenames:
        for s1, s2 in read_all_pairs(f):
            if s1 and s2:
                translations[s1, s2] += 1

    translations_as_list = [(count, translation)
                          for (translation, count)
                          in translations.iteritems()]

    translations_as_list.sort(reverse=True)

    for count, (s1, s2) in translations_as_list:
        if count < 2:
            break
        print count
        print s1.encode('utf-8')
        print s2.encode('utf-8')
        print
