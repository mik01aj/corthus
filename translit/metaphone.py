#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script that transliterates church-slavonic to polish.
It doesn't expand abbreviations, for that use another script.

Usage: ./metaphone.py <file>  (to use text file as input)
       ./metaphone.py -       (to use standard input)
"""


from __future__ import unicode_literals

import sys

metaphone_charset = "aeiou-bcdfhjkl7mnprstvz2"

pairs_cu = [

    ("w\т",  "ot"),
    ("о_у",  "u"),
    ("v'",   "i"),
    ('v"',   "i"),
    ("и",    "i"),
    ("е",    "e"),
    ("э",    "e"),
    ("jь",   "e"),
    ("ль",   "l"),
    ("лi",   "li"),
    ("ля",   "la"),
    ("лe",   "le"),
    ("лю",   "lu"),
    ("л",    "7"),
    ("а",    "a"),
    ("я",    "ja"),
    ("у",    "u"),
    ("ю",    "ju"),
    ("w",    "o"),
    ("о",    "o"),

    ("=",    ""),
    ("'",    ""),
    ("^",    ""),
    ("`",    ""),
    ("_",    ""),
    (":",    ""),
    (";",    ""),
    (",",    ""),
    (".",    ""),
    ("ь",    ""),
    ("\ъ",   ""),
    ("Ъ",    ""),
    ("ъ",    ""),

    ("s",    "z"),

    ("б",    "b"),
    ("ц",    "c"),
    ("д",    "d"),
    ("f",    "f"),
    ("ф",    "f"),
    ("гг",   "nh"),
    ("г",    "h"),
    ("х",    "h"),
    ("й",    "j"),
    ("к",    "k"),
    ("м",    "m"),
    ("н",    "n"),
    ("п",    "p"),
    ("р",    "r"),
    ("с",    "s"),
    ("т",    "t"),
    ("v",    "v"),
    ("в",    "v"),
    ("ы",    "i"),
    ("з",    "z"),
    ("ч",    "c"),
    ("щ",    "c"),
    ("ж",    "2"),
    ("ш",    "2"),
]

pairs_pl = [
    ("ę",    "e"),
    ("ą",    "o"),
    ("ó",    "u"),
    ("sz",   "2"),
    ("ż",    "2"),
    ("rz",   "2"),
    ("ś",    "2"),
    ("ź",    "z"),
    ("cz",   "c"),
    ("ć",    "c"),
    ("ł",    "7"),
    ("ń",    "n"),
    ("w",    "v"),
    ("g",    "h"),
    ]


def metaphone_generic(pairs, word):
    w = word
    for (pattern, replacement) in pairs:
        word = word.replace(pattern, replacement)
    if not word:
        return None
    for vowel in "aeiou":
        word = word[0] + word[1:].replace(vowel, '')
#    if len(word) > 5: #cu
#        for suffix in ["nj", "j", "m", "n"]:
#            if word.endswith(suffix):
#                word = word[:-len(suffix)]
    for c in word:
        if c not in metaphone_charset:
            return None
    return (word + '-----')[:5]

def metaphone_pl(word):
    return metaphone_generic(pairs_pl, word)

def metaphone_cu(word):
    return metaphone_generic(pairs_cu, word)

def metaphone(string):
    m_pl = metaphone_pl(string)
    m_cu = metaphone_cu(string)
    return tuple(m for m in (m_pl, m_cu) if m)

def test():
    cu_examples = [("прилjь'жнw",     "prile2no"),
                   ("богоро'дице",    "bohorodice"),
                   ("си^лы",          "si7y"),
                   ("глаго'лати",     "h7aho7ati"),
                   ("се'рдце",        "serce"),
                   ("_о=кая'ннаго",   "okajannaho"),
                   ("ми'лость",       "mi7ost"),
                   ("прибjь'жище",    "pribe2ice"),
                   ("мно'жества",     "mno2estva"),
                   ("фараw'ня",       "faraonja"),     # ?
                   ("бо'же'ственный", "bo2estvennij"),
                   ("безмjь'рную",    "bezmernuju"),
                   ("зача'ло",        "zaca7o"),
                   ("_е=vа'ггелiе",   "evanhelje"),
                   ("цjьлова'нiе",    "ce7ovanie"),
                   ("соверше'нiе",    "sover2enie"),
                   ("глагw'ланнымъ",  "h7aho7annim"),
                   ]
    groups = [("а='гг~лъ", "angel", "angieł"),
              ("_Е=vа'ггелiе", "Ευαγγελίον", "Ewangelia")]
    for value, expected in cu_examples:
        observed = metaphone(value)
        if observed != expected:
            print "for input %-15s expected %-15s, got %-15s" % \
                (value, expected, observed)
    print 'test done.'

if __name__ == '__main__':
    try:
        [filename] = sys.argv[1:]
        if filename == '-':
            inputFile = sys.stdin
        else:
            inputFile = open(filename)
    except ValueError:
        print __doc__
        sys.exit()
    for line in inputFile:
        line = line[:-1].decode('utf-8') # omitting '\n'
        words = []
        for word in line.split():
            words.append("/".join(metaphone(word)))
        print " ".join(words)
    inputFile.close()
