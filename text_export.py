#!/usr/bin/python

import sys
from Text import Text
from Alignment import Alignment

def export_for_giza(file1, file2, alignment_file, output1, output2):

    t1 = Text.from_file(file1, 'pl') # XXX
    t2 = Text.from_file(file2, 'cu')
    alignment = Alignment.from_file(alignment_file)

    bisents = []
    for s1, s2 in alignment.as_pairs(t1.as_sentences_flat(),
                                     t2.as_sentences_flat()):
        bisents.append((s1, s2))

    with open(output1, 'w') as f:
        for s, _ in bisents:
            f.write(s.encode('utf-8') + '\n')

    with open(output2, 'w') as f:
        for _, s in bisents:
            f.write(s.encode('utf-8') + '\n')

def export_for_hunalign(input_file, lang, output_file):
    t = Text.from_file(input_file, lang)
    with open(output_file, 'w') as f:
        for s in t.as_sentences(paragraph_separator='<p>'):
            f.write(s.encode('utf-8') + '\n')

if __name__ == '__main__':

    if sys.argv[1] == 'giza':
        (file1, file2, alignment_file, output1, output2) = sys.argv[2:]
        export_for_giza(file1, file2, alignment_file, output1, output2)
    elif sys.argv[1] == 'hunalign':
        (input_file, lang, output_file) = sys.argv[2:]
        export_for_hunalign(input_file, lang, output_file)
    else:
        print '?'
