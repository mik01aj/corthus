#!/usr/bin/python

import sys
from collections import defaultdict

def as_words(filenames):
    for filename in filenames:
        with open(filename) as f:
            for line in f.readlines():
                for w in line.decode('utf-8').split():
                    yield w

if __name__ == '__main__':

    test_file = sys.argv[1]
    filenames = sys.argv[2:]

    prefixes = defaultdict(lambda: 0)
    suffixes = defaultdict(lambda: 0)

    for word in as_words(filenames):
        for split in range(1, len(word)+1):
            prefixes[word[:split]] += 1
            suffixes[word[split:]] += 1

    print 'a'

    for word in as_words([test_file]):
        l = []
        for split in range(1, len(word)):
            score = prefixes[word[:split]] * suffixes[word[split:]]
            l.append((split, score))
        max_score = max(score for split, score in l)
        for split, score in l:
            print "%10s %-10s %4d %s" % \
                (word[:split],
                 word[split:],
                 score,
                 '*' if score == max_score else '')
        print

