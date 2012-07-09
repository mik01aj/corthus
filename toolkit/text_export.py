#!/usr/bin/python

import sys
from Text import Text
from Alignment import Alignment

"""
Exporting a Text to various formats. This script is also usable from
the command-line.

Usage:
    ./text_export.py giza <file1> <lang1> <file2> <lang2> \\
                          <alignment-file> <output1> <output2>
    ./text_export.py hunalign <input-file> <lang> <output-file>
"""

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

def export_for_hunalign(input_file, lang):
    t = Text.from_file(input_file, lang)
    for s in t.as_sentences(paragraph_separator='<p>'):
        #TODO transliterate
        print s.encode('utf-8')

if __name__ == '__main__':

    if sys.argv[1] == 'giza':
        export_for_giza(*sys.argv[1:])
    elif sys.argv[1] == 'hunalign':
        (input_file, lang) = sys.argv[2:]
        export_for_hunalign(input_file, lang)
    else:
        print __doc__
