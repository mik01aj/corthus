#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script that transliterates Greek to Polish. It assumes all the accents
in input are simplified (see simplify_el.py)

Usage: ./el2pl.py <file>  (to use text file as input)
       ./el2pl.py -       (to use standard input)
"""


from __future__ import unicode_literals

import sys

pairs = [
    ("αι",   "e"),
    ("αί",   "e\u0331"),

    ("εύ ",   "eu\u0331 "),
    ("εύς",   "eu\u0331s"),

    ("ου",   "u"),
    ("ού",   "u\u0331"),

    ("αι",   "e"),
    ("αί",   "e\u0331"),

    ("ει",   "i"),
    ("εί",   "i\u0331"),
    ("οι",   "i"),
    ("οί",   "i\u0331"),

    ("α",    "a"),
    ("ά",    "a\u0331"),
    ("β",    "w"),
    ("γ",    "g"),
    ("δ",    "d"),
    ("ε",    "e"),
    ("έ",    "e\u0331"),
    ("ζ",    "z"),
    ("η",    "i"),
    ("ή",    "i\u0331"),
    ("θ",    "f"),
    ("ι",    "i"),
    ("ί",    "i\u0331"),
    ("ϊ",    "i"),
    ("ΐ",    "i\u0331"),
    ("κ",    "k"),
    ("λ",    "l"),
    ("μ",    "m"),
    ("ν",    "n"),
    ("ξ",    "ks"),
    ("ο",    "o"),
    ("ό",    "o\u0331"),
    ("π",    "p"),
    ("ρ",    "r"),
    ("σ",    "s"),
    ("ς",    "s"),
    ("τ",    "t"),
    ("φ",    "f"),
    ("χ",    "ch"),
    ("ψ",    "ps"),    ("ω",    "o"),
    ("ώ",    "o\u0331"),
    ("'",    "'"),
    ("·",    "-"),
    (".",    "."),
    (":",    ":"),
    (";",    "?"),

    ("oυ",  "u"),
    ("aυ",  "aw"),
    ("oυ",  "ow"),
    ("eυ",  "ew"),
    ("iυ",  "iw"),
    ("aύ",  "a\u0331w"),
    ("oύ",  "o\u0331w"),
    ("eύ",  "e\u0331w"),
    ("iύ",  "i\u0331w"),

    ("υ",    "i"),
    ("ύ",    "i\u0331"),
    ("ϋ",    "i"),
    ("ΰ",    "i\u0331"),
]

def titlecase(string):
    if string:
        return string[0].upper() + string[1:]
    else:
        return ""

def el2pl(string):
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
        line = el2pl(line)
        print line.encode('utf-8')
    inputFile.close()
