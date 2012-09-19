#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
An aligner script.

Usage: ./aligner.py text.lang1.txt       text.lang2.txt       [options]
       ./aligner.py text.lang1.sentences text.lang2.sentences [options]
Options are:
    -text   writes the alignment as pretty-printed text
    -plot   plots the cost table to plot.png
    <i>,<j> forces sentences i in lang1 and j in lang2 to be aligned with
            each other. This is useful for correcting alignments by hand.
"""

from __future__ import division

import matplotlib
from math import log, exp, sqrt, pi, atan
import numpy as np
from cmath import polar
import sys

from PairManager import PairManager

matplotlib.use('Agg')

#_paragraph_separator = unicode('¶', 'utf-8')
_paragraph_separator = unicode('<p>')
_sentence_separator = unicode(' ♦ ', 'utf-8')

pair_manager = None #FIXME find some nice way to handle various languages


def calculate_cost(fragment1, fragment2):
    """Estimated -log(probability that fragment1 is translation of fragment2).
    Fragment1 and 2 are lists of sentences."""

    #XXX now it doesn't have anything to do with probability, as it
    # gives "probabilities" such as 2**30...

    #TODO write some conditions that should be always true, like:
    # * cost(s1, s2) + cost(¶, ¶) < cost(s1 + ¶, s2 + ¶)
    #                               (s+¶ can be even forbidden)
    # * cost(s1, s2) + cost('', s3) < cost(s1, s2 + s3) if s1 matches s2

    _s = _paragraph_separator

    (len1, len2) = (len(fragment1), len(fragment2))

    # addition/deletion
    if not fragment1 or not fragment2:
        assert len1 + len2 > 0
        #XXX assuming avg. 1 sentence in 32 is deleted
        real_sents = sum(sent != _s for sent in fragment1 + fragment2)
        if real_sents == 0:
            return 1
        return 20 * sqrt(real_sents)

    # if at least on of fragments begins or ends with paragraph separator
    elif (fragment1[0] == _s or fragment1[-1] == _s or
          fragment2[0] == _s or fragment2[-1] == _s):
        if fragment1 == fragment2:
            return -5
        else: # ¶ matched with something else
            return float('inf')

    # looking up pair
    elif pair_manager and pair_manager.has_pair(_sentence_separator.join(fragment1),
                                                _sentence_separator.join(fragment2)):
        return -10 * (len1+len2) #XXX

    # length-based evaluation
    else:
        (r, angle) = polar(complex(sum(len(s) for s in fragment1),
                                   sum(len(s) for s in fragment2)))
        angle -= pi/4
        join_penalty = len1 + len2 - 2
        # angle close to 0 is more probable than a big one (normal distribution)
        # a letter is around 2.5 bits of entropy
        #XXX this r should be multiplied by some big factor, so that it
        # would make a true normal distribution with angle**2
        return 1 + join_penalty + r*2.5 * angle**2


def plot_flat(fun, rangex, rangey, path=None, filename=None):
    import matplotlib.pyplot as plt

    print >> sys.stderr, 'Plotting...',
    sys.stderr.flush()

    size = max(rangex, rangey)/10
    fig = plt.figure(figsize=(size, size)) # in inches, @ 80dpi
    ax = fig.add_subplot(111)

    data = np.array([np.array([fun(x, y) for x in xrange(rangex)])
                     for y in xrange(rangey)])

    cax = ax.imshow(data, interpolation='nearest', cmap='gist_ncar')
    fig.colorbar(cax)
    if path:
        X, Y, Q = zip(*path)
        ax.scatter(X, Y,
                   #s=np.multiply(Q, 3),
                   s=1,
                   c='black')

    if filename:
        plt.savefig(filename)
    else:
        plt.show()
    print >> sys.stderr, '\rPlot done.      '


def align(seq1, seq2, plot_filename=None):

    len1, len2 = len(seq1), len(seq2)

    # cost[i][j] means sum of costs for seq1[0:i] and seq2[0:j]
    # in best possible alignment.
    # This also means -log(probability that sentences 0..i match 0..j).
    cost = [ [float('inf') for j in range(len2+1)]
             for i in range(len1+1) ]
    cost[0][0] = 0

    # an array to mark where did the best alignment come from
    prev = [ [None for j in range(len2+1)]
             for i in range(len1+1) ]

    fragment_lengths = ((1, 0), (0, 1), # skip a sentence
                        (1, 1),         # match 1-1
                        (1, 2), (2, 1), # match 1-2
                        (2, 2),         # match 2-2
                        (1, 3), (3, 1)) # match 3-1

    # i, j: sentence numbers
    for i in xrange(0, len1+1):
        print >> sys.stderr, "\ri=%d (%.f%%)" % (i, i*100/(len1+1)),
        sys.stderr.flush()
        for j in xrange(0, len2+1):

            # skipping some parts of the martix
            if len1 * len2 > 100 and abs(i/len1 - j/len2) > 0.4:
                continue

            # Iterating over possible matches.
            # Fragments tested end in i and j, respectively.
            # fl_i means "fragment length for i"
            for (fl_i, fl_j) in fragment_lengths:

                # fragments are seq1[_i:i] and seq2[_j:j]
                _i = i - fl_i
                _j = j - fl_j

                # if skipping, then skipping as one big jump
                #FIXME: this doesn't always find the best path,
                # because sometimes it is not worth it to jump over
                # just one sentence, so the jump won't start.
                # Perhaps some postprocessing will be needed to fix this.
                if (fl_i, fl_j) == (1, 0):
                    while prev[_i][_j] and prev[_i][_j][1] == _j:
                        _i = prev[_i][_j][0]
                elif (fl_i, fl_j) == (0, 1):
                    while prev[_i][_j] and prev[_i][_j][0] == _i:
                        _j = prev[_i][_j][1]

                if _i < 0 or _j < 0 or cost[_i][_j] is None:
                    continue

                new_cost = cost[_i][_j] + calculate_cost(seq1[_i:i],
                                                         seq2[_j:j])

                if new_cost < cost[i][j]:
                    #print >> sys.stderr, _i, i, _j, j
                    cost[i][j] = new_cost
                    prev[i][j] = (_i, _j)

    assert (i, j) == (len1, len2)
    path = [(i, j, 0.1)]
    while prev[i][j] is not None:
        c = cost[i][j]
        (i, j) = prev[i][j]
        c -= cost[i][j]
        path.append((i, j, c))

    if plot_filename:
        plot_flat(lambda x, y: cost[x][y],
                  len1+1, len2+1,
                  path,
                  filename=plot_filename)

    # total cost: - log(probability of given alignment); not normalized
    # the smaller the better
    print >> sys.stderr, "\rAlingment done. Total cost: " + str(cost[len1][len2])
    return reversed(path)


def iter_pairs(seq):
    prev = seq[0]
    for elem in seq[1:]:
        yield (prev, elem)
        prev = elem

def make_composed_alignment(seq1, seq2, forced_rungs):
    """Make an alignment with some rungs forced. It splits both
    sequences to pieces, and then composes an alignment from
    alignments on these parts. (Note: splitting text to parts also
    greatly improves performance)
    """
    forced_rungs = [(0,0)] + list(forced_rungs) + [(len(seq1), len(seq2))]
    def gen():
        yield (0, 0, 0.0) #?
        for (_fi, _fj), (fi, fj) in iter_pairs(forced_rungs):
#            if fi-_fi-1 <= 0 or fj-_fj-1 <= 0:
#                continue
            print >> sys.stderr, "Aligning %d:%d--%d:%d (%d--%d sents)..." % \
                (_fi+1, fi, _fj+1, fj, fi-_fi-1, fj-_fj-1)
            part_alignment = align(seq1[_fi+1:fi], seq2[_fj+1:fj])
            for (i, j, c) in part_alignment:
                yield (i+_fi+1, j+_fj+1, c)
#            print (fi, fj, 0.0)
    return list(gen())


# ----------------------------------------------------------------------

if __name__ == '__main__':

#    plot_flat(lambda x, y: similarity('a'*x, 'b'*y), 100, 100,
#              plot_filename='similarity.png')

    from Text import Text
    from Alignment import Alignment
    import re
    import codecs
    import os.path
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',
                        help='text folder')
    parser.add_argument('lang1')
    parser.add_argument('lang2')
#    parser.add_argument('--plot', action="store_true", default=False,
#                        help='plots the cost table to plot.png')
    parser.add_argument('--hand', action="store_true", default=None,
                        help='use file with hand-aligned sentence pairs')

    args = parser.parse_args()
    if args.folder.endswith('/'):
        args.folder = args.folder[:-1]
    for k, v in vars(args).items():
        print '%10s = %s' % (k, v)
    print

    # reading hand alignment
    forced_rungs = []
    if args.hand:
        filename = '%s/%s-%s.hand' % (args.folder, args.lang1, args.lang2)
        forced_rungs = Alignment.from_file(filename).as_ladder(with_costs=False)
        print >> sys.stderr, "%d hand-aligned pairs found in %s." % \
            (len(forced_rungs), filename)

    def read(filename, lang):
        with codecs.open(filename, encoding='utf-8') as f:
            return [l.strip() for l in f.readlines()]

    filename1 = args.folder + '/' + args.lang1 + '.sentences'
    filename2 = args.folder + '/' + args.lang2 + '.sentences'
    t1 = read(filename1, args.lang1)
    t2 = read(filename2, args.lang2)

    pairfile = os.path.join(os.path.dirname(__file__),
                            '../data/pairs.%s-%s' % (args.lang1, args.lang2))
    pair_manager = PairManager.from_file(pairfile)

    try:
        #a = align(t1, t2, plot_filename='plot.png' if '-plot' in opts else None)
        a = make_composed_alignment(t1, t2, forced_rungs)
        a = Alignment(a)
    finally:
        output_filename = '%s/%s-%s.my' % (args.folder, args.lang1, args.lang2)
        with open(output_filename, 'w') as f:
            for i, j, c in a.data:
                f.write("%d\t%d\t%.2f\n" % (i, j, c))
        print >> sys.stderr, "Wrote alignment to %s." % output_filename
