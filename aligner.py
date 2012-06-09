#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
An aligner script.

Usage: ./aligner.py text1 text2
"""

from __future__ import division

import matplotlib
from math import log, exp, sqrt, pi, atan
import numpy as np
from cmath import polar
import sys
from toolkit import Alignment, PairManager

matplotlib.use('Agg')

_paragraph_separator = unicode('¶', 'utf-8')
_sentence_separator = unicode(' ♦ ', 'utf-8')

pair_manager = PairManager.from_file('data/pairs.pl-cu') #XXX


def calculate_cost(fragment1, fragment2):
    """Estimated -log(probability that fragment1 is translation of fragment2).
    Fragment1 and 2 are lists of sentences."""

    #XXX now it doesn't have anything to do with probability, as it gives reults
    # such as 2**30...

    # paragraph separator with something
    if fragment1 == [_paragraph_separator] or fragment2 == [_paragraph_separator]:
        if fragment1 == fragment2:
            return -2
        elif not fragment1 or not fragment2: # ¶ with empty
            return 2
        else: # ¶ matched with something else
            return float('inf')

    # addition/deletion
    elif not fragment1 or not fragment2:
        num_sents = len(fragment1) + len(fragment2)
        assert num_sents > 0
        #XXX assuming avg. 1 sentence in 32 is deleted
        return 20 * sqrt(num_sents)

    elif pair_manager.has_pair(_sentence_separator.join(fragment1),
                               _sentence_separator.join(fragment2)):
        return -30 #XXX

    else:
        (r, angle) = polar(complex(sum(len(s) for s in fragment1),
                                   sum(len(s) for s in fragment2)))
        angle -= pi/4
        # angle close to 0 is more probable than a big one (normal distribution)
        # a letter is around 2.5 bits of entropy
        #FIXME this r should be multiplied by some big factor, so that it
        # would make a true normal distribution with angle**2
        return r*2.5 * angle**2


def plot_flat(fun, rangex, rangey, path=None, filename=None):
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(20, 20)) # in inches, @ 80dpi
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


def align(seq1, seq2, plot_filename=None):

    # cost[i][j] means sum of costs for seq1[0:i] and seq2[0:j]
    # in best possible alignment.
    # This also means -log(probability that sentences 0..i match 0..j).
    cost = [ [float('inf') for j in range(len(seq2)+1)]
             for i in range(len(seq1)+1) ]
    cost[0][0] = 0

    # an array to mark where did the best alignment come from
    prev = [ [None for j in range(len(seq2)+1)]
             for i in range(len(seq1)+1) ]

    #TODO problem: how to skip many sentences at once?

    fragment_lengths = ((1, 0), (0, 1), # skip a sentence
                        (1, 1),         # match 1-1
                        (1, 2), (2, 1), # match 1-2
                        (2, 2),         # match 2-2
                        (1, 3), (3, 1)) # match 3-1

    # i, j: sentence numbers
    for i in xrange(0, len(seq1)+1):
        print "\ri=%d (%.f%%)" % (i, i*100/(len(seq1)+1)),
        sys.stdout.flush()
        for j in xrange(0, len(seq2)+1):

            # skipping some parts of the martix
#            if abs(i/len(seq1) - j/len(seq2)) > 0.3:
#                continue

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
                # just one sentence, so the jump won't start
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
                    #print _i, i, _j, j
                    cost[i][j] = new_cost
                    prev[i][j] = (_i, _j)

    assert (i, j) == (len(seq1), len(seq2))
    path = [(i, j, 0.1)]
    while prev[i][j] is not None:
        c = cost[i][j]
        (i, j) = prev[i][j]
        c -= cost[i][j]
        path.append((i, j, c))
    path.append((0, 0, 0.1))

    if plot_filename:
        plot_flat(lambda x, y: cost[x][y],
                  len(seq1)+1, len(seq2)+1,
                  path,
                  filename=plot_filename)

    # total cost: - log(probability of given alignment); not normalized
    # the smaller the better
    print "Total cost: " + str(cost[len(seq1)][len(seq2)])
    return Alignment(reversed(path))


# ----------------------------------------------------------------------

if __name__ == '__main__':

#    plot_flat(lambda x, y: similarity('a'*x, 'b'*y), 100, 100,
#              plot_filename='similarity.png')

    from toolkit import Text, Alignment

    try:
        [filename1, filename2] = sys.argv[1:]
    except ValueError:
        print __doc__
        sys.exit()

    t1 = list(Text.from_file(filename1, lang='pl').as_sentences_flat())
    t2 = list(Text.from_file(filename2, lang='cu').as_sentences_flat())

    a = align(t1, t2, plot_filename='plot.png')

    a.pretty_print(t1, t2)

#    t1 = ('aa', 'aaa', 'aaaaa', 'a')
#    t2 = ('aa', 'aaaaaa', 'aa')
#    r = align(t1, t2)
#    print r
#    print r.quality

