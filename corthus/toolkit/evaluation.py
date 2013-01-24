#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division

import re
from TextFolder import TextFolder

def evaluate_alignment(aA, aB):

    fsA = list(aA.iter_tuples(*langs)) # A - tested alignment
    fsB = list(aB.iter_tuples(*langs)) # B - correct alignment

    def clean_next(it, c):
#        print '→', c
        s1, s2 = next(it)
        return (re.sub('\s*[¶♦]\s*', ' ', s1 if s1 else '').strip(),
                re.sub('\s*[¶♦]\s*', ' ', s1 if s2 else '').strip())

    itA = iter(fsA)
    itB = iter(fsB)
    sA1, sA2 = clean_next(itA, 'A')
    sB1, sB2 = clean_next(itB, 'B')

    intersection_len = 0
    text_len = len(sA1) + len(sA2)

    try:
        while True:

            common1, leftA, leftB = longest_common_substring(sA1, sB1)
            common2, _,     _     = longest_common_substring(sA2, sB2)
            intersection_len += common1 + common2

#            print ("A1 %-50s | B1 %-50s | %d" % (sA1[:50], sB1[:50], common1)).encode('utf-8')
#            print ("A2 %-50s | B2 %-50s | " % (sA2[:50], sB2[:50])).encode('utf-8')
#            print intersection_len / text_len

            if len(sA1) == 0:
                sA1, sA2 = clean_next(itA, 'A')
                text_len += len(sA1) + len(sA2)
            else:
                if leftA == 0:
                    sA1, sA2 = clean_next(itA, 'A')
                    text_len += len(sA1) + len(sA2)
                if leftB == 0:
                    try:
                        sB1, sB2 = clean_next(itB, 'B')
                    except StopIteration:
                        sA1, sA2 = clean_next(itA, 'A')
                        text_len += len(sA1) + len(sA2)
                if leftA != 0 and leftB != 0:
                    raise Exception(sA1, sB1)
    except StopIteration:
        pass
    return intersection_len / text_len


# from http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring
# modified: returns length of substring, and chars left to the end in s1 and s2
def longest_common_substring(s1, s2):
    i = s1.find(s2)
    if i != -1:
        return (len(s2), len(s1)-i+len(s2), 0)
    i = s2.find(s2)
    if i != -1:
        return (len(s1), 0, len(s2)-i+len(s1))
    M = [[0]*(1+len(s2)) for i in xrange(1+len(s1))]
    longest, x_longest, y_longest = 0, 0, 0
    for x in xrange(1,1+len(s1)):
        for y in xrange(1,1+len(s2)):
            if s1[x-1] == s2[y-1]:
                M[x][y] = M[x-1][y-1] + 1
                if M[x][y]>longest:
                    longest = M[x][y]
                    x_longest = x
                    y_longest = y
            else:
                M[x][y] = 0
    return (longest, len(s1)-x_longest, len(s2)-y_longest)



if __name__ == '__main__':
    from Alignment import Alignment
    from NewAlignment import NewAlignment

    langs = ('pl', 'cu')

    # A - tested alignment
    tf = TextFolder('texts/kanon_izr/')
    aA = NewAlignment.from_old_alignment(
        tf.get_alignment(langs, 'my'),
        langs,
        [tf.get_sentences(lang) for lang in langs])

    # B - correct alignment
    with open('texts/kanon_izr/everything') as f:
        aB = NewAlignment.read(f)

    baseline = NewAlignment()
    baseline.easy_append(pl=' '.join(tf.get_sentences('pl')),
                         cu=' '.join(tf.get_sentences('cu')))

    aB.pretty_print('pl', 'cu')

    print evaluate_alignment(aA, aB)
    print evaluate_alignment(baseline, aB)
