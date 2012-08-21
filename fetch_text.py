#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Usage:
    ./fetch_text.py text langs
"""

import sys
from toolkit import Text, Alignment
from toolkit.translit import metaphone_text, translit_pl, expand_cu
import codecs

def fetch_sentences(basename, lang):
    assert lang in ('pl', 'cu', 'cue', 'cum', 'cut', 'el', 'elm', 'elt')
    real_lang = lang[:2]
    transformation = lang[2:]

    try:
        with file("texts/%s.%s.sentences" % (basename, real_lang)) as f:
            t = f.readlines()
    except IOError:
        t = Text.from_file("texts/%s.%s.txt" % (basename, real_lang), lang=real_lang).as_sentences_flat()

    if transformation:
        if transformation == 'm':
            t = [' '.join(metaphone_text(s, lang=real_lang)) for s in t]
        elif transformation == 't':
            t = [translit_pl(s, real_lang) for s in t]
        elif transformation == 'e':
            t = [expand_cu(s, numbers=True) for s in t]

    return t

def transpose(arr):
    return zip(*arr)

def fetch_alignment(basename, langs, backend='hunalign'):
    assert langs
    real_langs = list(set(lang[:2] for lang in langs))
    assert len(real_langs) < 3, "langs>=3 not implemented"

    if len(real_langs) == 1:
        text_len = len(fetch_sentences(basename, real_langs[0]))
        return Alignment.create_straight(text_len, len(langs))
    else:
        try:
            a = Alignment.from_file("texts/%s.%s-%s.%s" %
                                    (basename, real_langs[0], real_langs[1], backend))
        except IOError:
            real_langs.reverse()
            a = Alignment.from_file("texts/%s.%s-%s.%s" %
                                    (basename, real_langs[0], real_langs[1], backend))
        columns = transpose(a.data)
        columns_map = { real_langs[0] : columns[0],
                        real_langs[1] : columns[1] }

        chosen_columns = [columns_map[lang[:2]] for lang in langs]
        chosen_columns.append(columns[2])

        return Alignment(transpose(chosen_columns))

if __name__ == '__main__':
    try:
        [basename, langs] = sys.argv[1:]
        langs = langs.split('-')
    except ValueError:
        print >> sys.stderr; __doc__

    fetch_alignment(basename, langs).pretty_print(*[fetch_sentences(basename, lang)
                                                    for lang in langs])
