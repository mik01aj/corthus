#!/usr/bin/python

"""
Example usage:

./experimental_stemmer.py texts/kanon_izr/cu.txt texts/octoih/1_*/cu.txt
                          (test file)            (learning files)
"""

from __future__ import division

import sys
from collections import defaultdict
from math import log

def as_words(filenames):
    for filename in filenames:
        with open(filename) as f:
            for line in f.readlines():
                for w in line.decode('utf-8').split():
                    yield w

if __name__ == '__main__':

    try:
        test_file = sys.argv[1]
        filenames = sys.argv[2:]
    except:
        print __doc__
        sys.exit()

    prefixes = defaultdict(lambda: 0.00001)
    suffixes = defaultdict(lambda: 0.00001)

    for word in as_words(filenames):
        for split in range(0, len(word)+1):
            prefixes[word[:split]] += 1
            suffixes[word[split:]] += 1

    print 'a'

    for word in as_words([test_file]):
        l = []
        for split in range(0, len(word)+1):
            # log(frequency) * length ~= log("non-randomness of char sequence")
            score = (log(prefixes[word[:split]]) * split +
                     log(suffixes[word[split:]]) * (len(word) - split))
            l.append((split, score))
        max_score = max(score for split, score in l)
        for split, score in l:
            print ("%25s %s%8.3f" % \
                       (word[:split] + ' ' +  word[split:],
                        '*' if score == max_score else ' ',
                        score)).encode('utf-8')
        print

