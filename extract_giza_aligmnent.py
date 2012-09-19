#!/usr/bin/python

"""
what I did:

from NewAlignment.py:

with open('texts/kanon_izr/everything') as f:
    a = NewAlignment.read(f)
with open('/tmp/sents_cu', 'w') as f1:
    with open('/tmp/sents_el', 'w') as f2:
        a.export_sentences_for_giza('cu', 'el', f1, f2)

./plain2snt.out /tmp/sents_cu /tmp/sents_el
./snt2cooc.out /tmp/sents_cu.vcb /tmp/sents_el.vcb /tmp/sents_cu_sents_el.snt > /tmp/cooc
./GIZA++ -S /tmp/sents_cu.vcb -T /tmp/sents_el.vcb -C /tmp/sents_cu_sents_el.snt -p0 0.98 -CoocurrenceFile /tmp/cooc -o /tmp/dict

"""

from __future__ import unicode_literals

import sys
import math
import re

fn = sys.argv[1] # '/tmp/dict'

def group_elems(seq, cnt):
    it = iter(seq)
    while True:
        l = []
        try:
            for i in range(cnt):
                l.append(next(it))
        finally:
            if l:
                yield l

def parse_alignment_line(line):
    it = iter(line.split())
    while True:
        word = next(it).decode('utf-8')
        assert next(it) == '({'
        nums = []
        token = next(it)
        while token != '})':
            nums.append(int(token))
            token = next(it)
        yield (word, nums)

# example
"""
# Sentence pair (26) source length 17 target length 22 alignment score : 1.33525e-16
epivlepso e ovmeneia panimnite feotoke - epi tin emin halepin tu somatos kakosin - ke iase tis psihis mu to alhos -
NULL ({ }) prizri ({ 1 }) b7ahoserdiem ({ 2 3 }) vsepetaja ({ 4 }) bohorodice ({ 5 }) - ({ 6 }) na ({ 7 }) moe ({ 8 }) lutoe ({ 9 }) telese ({ 10 11 12 }) oz7oblenie ({ 13 }) - ({ 14 }) i ({ 15 }) isceli ({ 16 17 }) du2i ({ 18 }) moeja ({ 19 20 }) bolezn ({ 21 }) - ({ 22 })
"""

sents = []

with open(fn + '.A3.final') as f:
    for comment, l1, l2 in group_elems(f, 3):
        sent = []
        m = re.match('# Sentence pair \((\d+)\) source length (\d+) target length (\d+) alignment score : (\d.\d+e?-?\d*)$',
                     comment.strip())
        summed_length = int(m.group(2)) + int(m.group(3))
        score = float(m.group(4))
        l1 = l1.decode('utf-8').split()
        for word, nums in parse_alignment_line(l2):
            matched_words = ' '.join(l1[i-1] for i in nums)
            sent.append((word, matched_words))
        sents.append((sent, score, summed_length))

# pretty-printing -----------------------------------------

def pad((string1, string2)):
    maxlen = max(len(string1), len(string2))
    return (string1 + ' '*(maxlen-len(string1)),
            string2 + ' '*(maxlen-len(string2)))

for sent, score, summed_length in sents:
    print score, summed_length
    pairs = map(pad, sent)
    to_print = []
    for w1, w2 in pairs:
        if sum(len(w) for (w, _) in to_print) + len(w1) > 80:
            s1, s2 = zip(*to_print)
            print ' '.join(s1)
            print ' '.join(s2)
            to_print = []
        to_print.append((w1, w2))
    s1, s2 = zip(*to_print)
    print ' '.join(s1)
    print ' '.join(s2)
    print

