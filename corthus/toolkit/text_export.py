#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Exporting a Text to various formats. This script is also usable from
the command-line.

Usage:
    ./text_export.py giza <file1> <lang1> <file2> <lang2> \\
                          <alignment-file> <output1> <output2>
    ./text_export.py hunalign <input-file> <lang>
    ./text_export.py sentences <input-file> <lang>
"""

from __future__ import unicode_literals

import sys
from Text import Text
from Alignment import Alignment


def extract_bisents(file1, lang1, file2, lang2, alignment_file):
    assert isinstance(lang1, (unicode, str)) and len(lang1)==2
    assert isinstance(lang2, (unicode, str)) and len(lang2)==2
    t1 = Text.from_file(file1, lang1)
    t2 = Text.from_file(file2, lang2)
    alignment = Alignment.from_file(alignment_file)
    bisents = alignment.as_pairs(t1.as_sentences_flat(),
                                 t2.as_sentences_flat())
    return bisents

def export_for_giza(file1, lang1, file2, lang2, alignment_file,
                    output1, output2):

    bisents = extract_bisents(file1, lang1, file2, lang2, alignment_file)

    with open(output1, 'w') as f:
        for s, _ in bisents:
            f.write(s.encode('utf-8') + '\n')

    with open(output2, 'w') as f:
        for _, s in bisents:
            f.write(s.encode('utf-8') + '\n')

def export_sentences(input_file, lang, export_type):
    from translit.metaphone import metaphone
    t = Text.from_file(input_file, lang)
    for s in t.as_sentences(paragraph_separator='¶'):
        if export_type == 'hunalign':
            if s == '¶':
                s = '<p>'
            else:
                s = ' '.join(metaphone(w) for w in s.split())
        print s.encode('utf-8')

if __name__ == '__main__':

    if sys.argv[1] == 'giza':
        export_for_giza(*sys.argv[1:])
    elif sys.argv[1] in ['hunalign', 'sentences']:
        (input_file, lang) = sys.argv[2:]
        export_sentences(input_file, lang, sys.argv[1])
    else:
        print >> sys.stderr, __doc__
        exit(1)
