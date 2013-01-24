#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script that transliterates church-slavonic to English.
It doesn't expand abbreviations, for that use another script.

Usage: ./cu2pl.py <file>  (to use text file as input)
       ./cu2pl.py -       (to use standard input)
"""


from __future__ import unicode_literals

import sys

pairs = [
    (r"'",    "´"),
    (r"`",    "´"),
    (r"^",    "´"),
    (r"=",    ""),
    (r"_",    ""),

    (r"«",    "“"),
    (r"»",    "”"),
    (r"№",    "#"),
    (r"–",    "-"),
    (r";",    "?"),

    (r"Ь",    "'"),
    (r"ь",    "'"),
    (r"Ъ",    ""),
    (r"ъ",    ""),

    (r"0",    "0"),
    (r"1",    "1"),
    (r"2",    "2"),
    (r"3",    "3"),
    (r"4",    "4"),
    (r"5",    "5"),
    (r"6",    "6"),
    (r"7",    "7"),
    (r"8",    "8"),
    (r"9",    "9"),

    (r"а",    "a"),
    (r"б",    "b"),
    (r"C",    "C"),
    (r"c",    "c"),
    (r"д",    "d"),
    (r"jь",   "e"),
    (r"е",    "e"),
    (r"э",    "e"),
    (r"f",    "f"),
    (r"ф",    "f"),
    (r"г",    "g"),
    (r"х",    "h"),
    (r"i",    "i"),
    (r"v\"",  "i"),
    (r"v'",   "i"),
    (r"и",    "i"),
    (r"й",    "j"),
    (r"к",    "k"),
    (r"л",    "l"),
    (r"м",    "m"),
    (r"н",    "n"),
    (r"_о",   "o"),
    (r"w",    "o"),
    (r"о",    "o"),
    (r"_п",   "p"),
    (r"п",    "p"),
    (r"Q",    "Q"),
    (r"q",    "q"),
    (r"р",    "r"),
    (r"\ъс",  "s"),
    (r"с",    "s"),
    (r"т",    "t"),
    (r"\ъу",  "u"),
    (r"о_у",  "u"),
    (r"у",    "u"),
    (r"v",    "v"),
    (r"в",    "v"),
    (r"X",    "X"),
    (r"x",    "x"),
    (r"Y",    "Y"),
    (r"y",    "y"),
    (r"ы",    "y"),
    (r"s",    "z"),
    (r"з",    "z"),
    (r"\ъ_о", "o"),
    (r"\ъw",  "w"),
    (r"ч",    "ch"),
    (r"я",    "ia"),
    (r"ё",    "io"),
    (r"ю",    "iu"),
    (r"w\т",  "ot"),
    (r"ш",    "sh"),
    (r"ц",    "ts"),
    (r"jа",   "ya"),
    (r"\ъи",  "yi"), # паерок + и
    (r"ж",    "zh"),
    (r"чы",   "chi"),
    (r"щ",    "sch"),
    (r"шя",   "sha"),
    (r"шы",   "shi"),
    (r"гг",   "ng"),  # this is not always correct (а'ггелъ)
    (r"щы",   "schi"),

    (r"а~",   "1"), # numbers
    (r"в~",   "2"),
    (r"г~",   "3"),
    (r"д~",   "4"),
    (r"е~",   "5"),
    (r"м~",   "40"),
]

# sort pairs to have longest patterns first
pairs.sort(cmp=lambda (x, x2), (y, y2): -cmp(len(x), len(y)))

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
        line = line.decode('utf-8')
        #TODO uppercase letters
        for (pattern, replacement) in pairs:
            line = line.replace(pattern, replacement)
        print line[:-1].encode('utf-8') # omitting '\n'
    inputFile.close()
