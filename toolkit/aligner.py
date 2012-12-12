#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
An aligner script.

It aligns two sentence-splitted texts.
"""

from __future__ import division

from math import log, exp, sqrt, pi, atan
from collections import defaultdict
import sys

from PairManager import PairManager
from preprocess import preprocess

_paragraph_separator = unicode('¶', 'utf-8')
#_paragraph_separator = unicode('<p>')
_sentence_separator = unicode(' ♦ ', 'utf-8')

pair_manager = None


def calculate_cost(fragment1, fragment2):
    """Estimated -log(p, base=2), where p = probability that fragment1
    is translation of fragment2. Fragment1 and 2 are lists of
    sentences."""

    _ps = _paragraph_separator
    _ss = _sentence_separator

    (len1, len2) = (len(fragment1), len(fragment2))
    pair = (_ss.join(fragment1),
            _ss.join(fragment2))

    # estimated probabilities for unknown pairs
    avg_word_match_prob = 0.5
    avg_word_skip_prob = 0.2
    avg_word_skip_in_sent_prob = 0.25
    avg_sent_join_prob = 0.008 # (same cost as skipping 3 words)

    # addition/deletion
    if not fragment1 or not fragment2:
        assert len1 + len2 > 0
        if fragment1 + fragment2 == [_ps]:
            return 0.5 # p ~= 0.7
        num_words = len(' '.join(fragment1 + fragment2).split())
        return -(log(avg_word_skip_in_sent_prob, 2) * num_words +
                 log(pair_manager.hapax_prob))

    # if at least one of fragments begins or ends with paragraph separator
    elif (fragment1[0] == _ps or fragment1[-1] == _ps or
          fragment2[0] == _ps or fragment2[-1] == _ps):
        if fragment1 == fragment2:
            return 0 # -log(1)
        else: # ¶ matched with something else
            return float('inf') # -log(0)

    # looking up pair
    elif pair_manager and pair_manager.has_pair(*pair):
        return -log(pair_manager.get_pair_prob(*pair))

    # length-based evaluation
    else:
        num_words1 = len(pair[0].split())
        num_words2 = len(pair[1].split())
        if num_words1 > num_words2:
            num_words1, num_words2 = num_words2, num_words1
        # now num_words1 <= num_words2

        return -(log(pair_manager.hapax_prob) +
                 log(avg_sent_join_prob, 2) * (len1 + len2 - 2) +
                 log(avg_word_match_prob, 2) * num_words1 +
                 log(avg_word_skip_prob, 2) * (num_words2 - num_words1))


def align(seq1, seq2, only_bisents=False,
          cost_function=calculate_cost,
          output_line=''):

    len1, len2 = len(seq1), len(seq2)

    # cost[i][j] means sum of costs for seq1[0:i] and seq2[0:j]
    # in best possible alignment.
    # This also means -log(probability that sentences 0..i match 0..j).
    global cost # global var for plotting
    cost = [ [float('inf') for j in range(len2+1)]
             for i in range(len1+1) ]
    cost[0][0] = 0

    # an array to mark where did the best alignment come from
    prev = [ [None for j in range(len2+1)]
             for i in range(len1+1) ]

    if only_bisents:
        fragment_lengths = ((1, 0), (0, 1), # skip a sentence
                            (1, 1))         # match 1-1
    else:
        fragment_lengths = ((1, 0), (0, 1), # skip a sentence
                            (2, 0), (0, 2), # skip 2
                            (1, 1),         # match 1-1
                            (1, 2), (2, 1), # match 1-2
                            (2, 2),         # match 2-2
                            (1, 3), (3, 1)) # match 3-1

    # i, j: sentence numbers
    for i in xrange(0, len1+1):

        print >> sys.stderr, "\r%si=%d (%.f%%)" % (output_line, i, i*100/(len1+1)),
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

                if _i < 0 or _j < 0 or cost[_i][_j] is None:
                    continue

                new_cost = cost[_i][_j] + cost_function(seq1[_i:i],
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

    # total cost: - log(probability of given alignment); not normalized
    # the smaller the better
    total_cost = cost[len1][len2]
    avg_cost = total_cost / len(path)
    print >> sys.stderr, ("\r%sdone. Total cost:%7.2f, avg:%5.2f" %
                          (output_line, total_cost, avg_cost))
    return list(reversed(path))


def iter_pairs(seq):
    """[1, 2, 3, 4] -> [(1, 2), (2, 3), (3, 4)]"""
    prev = seq[0]
    for elem in seq[1:]:
        yield (prev, elem)
        prev = elem


def set_languages(l1, l2):
    global lang1, lang2, pair_manager
    lang1 = l1
    lang2 = l2
    pairfile = os.path.join(os.path.dirname(__file__),
                            '../data/pairs.%s-%s' % (args.lang1, args.lang2))
    pair_manager = PairManager.from_file(pairfile)


def find_matches(seq1, seq2, threshold, pair_count=None):
    #NOTE: this doesn't work for 1-to-many pairs
    matches = (set(), set())
    for prob, s1, s2 in pair_manager.iter_best_pairs(threshold, pair_count):
        if s1 == _paragraph_separator or s2 == _paragraph_separator:
            continue
        matches[0].add(s1)
        matches[1].add(s2)
        threshold = prob # lowering threshold

    # we'll align `sents` and use `indices` list to get original indices in `seq*`
    sents   = ([], [])
    indices = ([], []) # seq1[indices[0][x]] == sents[0][x]
    occurences = (defaultdict(lambda: 0),
                  defaultdict(lambda: 0)) # counts of occurences of sentences
    for i, seq in enumerate([seq1, seq2]):
        sents[i].append('start')
        indices[i].append(0)
        for sent_num, sent in enumerate(seq):
            if sent in matches[i]:
                occurences[i][sent] += 1
                sents[i].append('x ' * (sent_num - indices[i][-1]))
                sents[i].append(sent)
                indices[i].append(None)
                indices[i].append(sent_num)
#            assert seq[indices[i][-1]] == sents[i][-1]

    for i, seq in enumerate([seq1, seq2]):
        print >> sys.stderr, "Matched %d of %d sents of text%d (%.1f%%)" % \
            (len(sents[i]), len(seq), i+1, len(sents[i])*100/len(seq))

    alignment_indices = align(*sents, output_line='Prealign... ')

#    Alignment(alignment_indices).pretty_print(*sents)

    for (i, j, cost) in alignment_indices[:-1]:
        if cost < -log(threshold, 2):
            print ("%3d %-35s | %3d %-35s | p=%.2f" %
                   (indices[0][i], sents[0][i][:35],
                    indices[1][j], sents[1][j][:35], 2**-cost))
            yield indices[0][i], indices[1][j], cost


def make_composed_alignment(seq1, seq2, forced_rungs):
    """Make an alignment with some rungs forced. It splits both
    sequences to pieces, and then composes an alignment from
    alignments on these parts. (Note: splitting text to parts also
    greatly improves performance)
    """
    forced_rungs = [(0, 0, 0)] + list(forced_rungs) + [(len(seq1), len(seq2), 0)]
    def gen():
        yield (0, 0, 0.0) #?
        for (_fi, _fj, _c), (fi, fj, c) in iter_pairs(forced_rungs):
#            if fi-_fi-1 <= 0 or fj-_fj-1 <= 0:
#                continue
            yield (_fi+1, _fj+1, _c)
            info = ("Aligning %3d:%-3d--%3d:%-3d (%3d--%-3d sents)... " %
                    (_fi+1, fi, _fj+1, fj, fi-_fi-1, fj-_fj-1))
            part_alignment = align(seq1[_fi+1:fi], seq2[_fj+1:fj],
                                   output_line=info)
            for (i, j, c) in part_alignment[1:]:
                yield (i+_fi+1, j+_fj+1, c)
#            print (fi, fj, 0.0)
    return list(gen())


# ----------------------------------------------------------------------

if __name__ == '__main__':

    from Text import Text
    from Alignment import Alignment
    from TextFolder import TextFolder
    import os.path
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', help='text folder')
    parser.add_argument('lang1')
    parser.add_argument('lang2')
    parser.add_argument('--prealign', action="store_true", default=False,
                        help='split file into pieces, based on common sentence pairs')
    parser.add_argument('--hand', action="store_true", default=None,
                        help='use file with hand-aligned sentence pairs (??-??.hand)')
    parser.add_argument('--plot', metavar='FILE.png', action="store", default=False,
                        help='plots the matrix of accumulated costs')
    parser.add_argument('--plot-sim', metavar='FILE.png', action="store", default=False,
                        help='plots the matrix of pair costs')
    parser.epilog = 'options --hand and --prealign together may cause conflicts, beware!'

    args = parser.parse_args()

    print >> sys.stderr
    print >> sys.stderr, ("=== Aligning %s, %s-%s ===" %
                          (args.folder, args.lang1, args.lang2))

    set_languages(args.lang1, args.lang2)
    tfolder = TextFolder(args.folder)
    t1 = map(preprocess, tfolder.get_sentences(args.lang1))
    t2 = map(preprocess, tfolder.get_sentences(args.lang2))

    # reading hand alignment
    forced_rungs = []
    if args.hand:
        hand_alignment = tfolder.get_alignment([args.lang1, args.lang2],
                                               backend='hand')
        forced_rungs = hand_alignment.as_ladder()
        print >> sys.stderr, "%d hand-aligned pairs found." % len(forced_rungs)
    # prealign
    if args.prealign:
        pre_alignment = list(find_matches(t1, t2, threshold=0.5, pair_count=100))
        forced_rungs.extend(pre_alignment)
        print >> sys.stderr, "%d sentence pairs matched." % len(pre_alignment)
    forced_rungs = sorted(set(forced_rungs))

    try:
        a = None
        a = make_composed_alignment(t1, t2, forced_rungs)
        a = Alignment(a)
    finally:
        output_filename = '%s/%s-%s.my' % (args.folder, args.lang1, args.lang2)
        if not a:
            raise SystemExit
        with open(output_filename, 'w') as f:
            for i, j, c in a.data:
                f.write("%d\t%d\t%.2f\n" % (i, j, c))
        print >> sys.stderr, "Wrote alignment to %s." % output_filename
        c = a.summed_cost()
        print >> sys.stderr, "Total cost", c, "avg", c/len(a.data)

        if args.plot:
            import plot
            plot.plot_cost_matrix(cost,
                                  a.as_ladder(),
                                  plot_filename=args.plot)

        if args.plot_sim:
            import plot
            c = [[0 for s2 in t2]
                 for s1 in t1]
            _i, _j = 0, 0
            for i, j, _ in forced_rungs + [(len(t1), len(t2), 0)]:
                for mi in range(_i, i):
                    for mj in range(_j, j):
                        c[mi][mj] = calculate_cost([t1[mi]], [t2[mj]])
                _i, _j = i, j
#            a2 = Alignment.from_file('/tmp/pl-cu.new')
            plot.plot_cost_matrix(c,
                                  path=a.as_ladder(with_costs=True),
#                                  path2=a2.as_ladder(with_costs=True),
                                  plot_filename=args.plot_sim)
