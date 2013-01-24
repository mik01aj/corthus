#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script that transliterates church-slavonic to Polish.
It doesn't expand abbreviations, for that use another script.

Usage: ./cu2pl.py <file>  (to use text file as input)
       ./cu2pl.py -       (to use standard input)
"""


from __future__ import unicode_literals

import sys

pairs = [
    (r"jь",   "je"),
    (r"_е",   "je"),
    (r"е",    "je"),
    (r"э",    "je"),

    (r"\ъи",  "ji"), # и̾
    (r"i",    "i"),
    (r'v"',   "i"),
    (r"v'",   "i"),
    (r"v=",   "i"),
    (r"и",    "i"),

    (r"'",    "\u0331"),
    (r"`",    "\u0331"),
    (r"^",    "\u0331"),
    (r"=",    ""),
    (r";",    "?"),

    (r"ль",   "l"),
    (r"лi",   "li"),
    (r"ля",   "lia"),
    (r"лje",  "lie"),
    (r"лю",   "liu"),
    (r"л",    "ł"),

    (r"s",    "z"),
    (r"jа",   "ja"),
    (r"шя",   "sza"),
    (r"гг",   "ng"),  # this is not always correct (а'ггелъ)
    (r"w\т",  "ot"),
    (r"о_у",  "u"),

    (r"а",    "a"),
    (r"б",    "b"),
    (r"ц",    "c"),
    (r"д",    "d"),
    (r"f",    "f"),
    (r"ф",    "f"),
    (r"г",    "g"),
    (r"х",    "ch"),
    (r"й",    "j"),
    (r"к",    "k"),
    (r"м",    "m"),
    (r"нje",   "nie"),
    (r"н",    "n"),
    (r"w",    "o"),
    (r"о",    "o"),
    (r"п",    "p"),
    (r"р",    "r"),
    (r"с",    "s"),
    (r"т",    "t"),
    (r"у",    "u"),
    (r"v",    "w"),
    (r"в",    "w"),
    (r"ы",    "y"),
    (r"з",    "z"),
    (r"ж",    "ż"),
    (r"ч",    "cz"),
    (r"я",    "ja"),
    (r"ю",    "ju"),
    (r"ш",    "sz"),
    (r"щ",    "szcz"),

    ("cje",   "ce"),
    ("żje",   "że"),
    ("szje",  "sze"),
    ("czje",  "cze"),

    ("pj",    "pi"),
    ("bj",    "bi"),
    ("fj",    "fi"),
    ("wj",    "wi"),
    ("sj",    "si"),
    ("cj",    "ci"),
    ("hj",    "hi"),
    ("nj",    "ni"),
    ("mj",    "mi"),
    ("lj",    "li"),
    ("łj",    "łi"),
    ("kj",    "ki"),
    ("gj",    "gi"),
    ("tj",    "ti"),
    ("dj",    "di"),
    ("szj",   "szi"),
    ("żj",    "żi"),
    ("czj",   "czi"),
    ("rj",    "ri"),

    ("Ь",    "'"),
    ("ь",    "'"),
    ("n'",    "ń"),

#    ("czi",   "czy"),

#    ("ii",    "ij"),

    (r"\ъ",   ""),
    (r"Ъ",    ""),
    (r"ъ",    ""),
    (r"_",    ""),
]

def titlecase(string):
    if string:
        return string[0].upper() + string[1:]
    else:
        return ""

def cu2pl(string):
    for (pattern, replacement) in pairs:
        string = string.replace(pattern, replacement)
        string = string.replace(titlecase(pattern), titlecase(replacement))
    return string

if __name__ == '__main__':
    try:
        [filename] = sys.argv[1:]
        if filename == '-':
            inputFile = sys.stdin
        else:
            inputFile = open(filename)
    except ValueError:
        print __doc__
        print "Patterns replaced (in this order):"
        for (a, b) in pairs:
            print ("%20s → %s" % (a, b)).encode('utf-8')
        sys.exit()
    for line in inputFile:
        line = line[:-1].decode('utf-8') # omitting '\n'
        line = cu2pl(line)
        print line.encode('utf-8')
    inputFile.close()
