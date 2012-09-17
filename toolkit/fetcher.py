#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Usage:
    ./fetcher.py text langs [backend]
"""

import sys
from Text import Text
from Alignment import Alignment
from translit import metaphone_text, translit_pl, expand_cu
from merge_alignments import merge_3_alignments

def fetch_sentences(basename, lang):
    assert lang in ('pl', 'plm',
                    'cu', 'cum', 'cut', 'cue',
                    'el', 'elm', 'elt'), "invalid lang " + lang

    real_lang = lang[:2]
    transformation = lang[2:]

    basename_with_lang = ("%s/%s" % (basename, real_lang))

    try:
        #TODO maybe open ready metaphone files?
        with file("%s.sentences" % basename_with_lang) as f:
            t = [line.decode('utf-8').strip() for line in f.readlines()]
    except IOError:
        t = Text.from_file("%s.txt" % basename_with_lang,
                           lang=real_lang).as_sentences_flat()

    if transformation:
        if transformation == 'm':
            return [metaphone_text(s, lang=real_lang) for s in t]
        elif transformation == 't':
            return [translit_pl(s, real_lang) for s in t]
        elif transformation == 'e':
            return [expand_cu(s, numbers=True) for s in t]
    return t

def _transpose(arr):
    return zip(*arr)

def fetch_alignment(basename, langs, backend='hunalign'):
    assert langs
    real_langs = list(set(lang[:2]
                          for lang in langs))

    if len(real_langs) == 1:
        text_len = len(fetch_sentences(basename, real_langs[0]))
        return Alignment.create_straight(text_len, len(langs))
    elif len(real_langs) == 2:
        try:
            a = Alignment.from_file("%s/%s-%s.%s" %
                                    (basename, real_langs[0], real_langs[1], backend))
        except IOError:
            real_langs.reverse()
            a = Alignment.from_file("%s/%s-%s.%s" %
                                    (basename, real_langs[0], real_langs[1], backend))

    else: # len(real_langs) == 3 :(
        a1 = Alignment.from_file('%s/pl-cu.%s' % (basename, backend)).as_ladder()
        a2 = Alignment.from_file('%s/cu-el.%s' % (basename, backend)).as_ladder()
        a3 = Alignment.from_file('%s/pl-el.%s' % (basename, backend)).as_ladder()
        a3 = [(b, a) for (a, b) in a3] # reversed
        a = merge_3_alignments(a1, a2, a3)
        real_langs = ['pl', 'cu', 'el'] # needed later

    columns = _transpose(a.data)
    columns_map = { real_langs[i] : columns[i]
                    for i in range(len(real_langs)) }

    # common part for 2 and 3
    chosen_columns = [columns_map[lang[:2]] for lang in langs]
    chosen_columns.append(columns[2])
    return Alignment(_transpose(chosen_columns))


#def fetch_grouped_list - TODO

if __name__ == '__main__':
    try:
        if len(sys.argv) == 3:
            [basename, langs] = sys.argv[1:]
            backend = 'hunalign'
        else:
            [basename, langs, backend] = sys.argv[1:]
        langs = langs.split('-')
    except ValueError:
        print >> sys.stderr, __doc__
        sys.exit(1)

    a = fetch_alignment(basename, langs, backend)
    a.pretty_print(*[fetch_sentences(basename, lang)
                     for lang in langs])
