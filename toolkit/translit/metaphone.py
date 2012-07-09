#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script that transliterates church-slavonic to polish.
It doesn't expand abbreviations, for that use another script.

Usage: ./metaphone.py <file>  (to use text file as input)
       ./metaphone.py -       (to use standard input)
"""


from __future__ import unicode_literals

from simplify_el import simplify_el
from expand_cu import expand_cu
import sys
import re
import unicodedata

WARNINGS_ENABLED = True # changed also by metaphone function

metaphone_charset = "aeiou-#?bcdfhjkl7mnprstvz2"

ignored_chars = ".,:;!?@΄᾽῞∙··()[]{}<>«»„”\"–\xad*…" # \xad - soft hyphen
ignored_chars_regex = re.compile("["+re.escape(ignored_chars)+"]", re.UNICODE)

pairs_pl = [
    ("ę",   "e"),
    ("ą",   "o"),
    ("ó",   "u"),
    ("g",   "h"),
    ("ch",  "h"),
    ("dz",  "d"),
    ("dż",  "d"),
    ("sz",  "2"),
    ("ż",   "2"),
    ("rz",  "2"),
    ("ś",   "2"),
    ("ź",   "z"),
    ("cz",  "c"),
    ("ć",   "c"),
    ("ł",   "7"),
    ("ń",   "n"),
    ("w",   "v"),
    ("y",   "i"),
    ("é",   "e"), # used in old Polish
    ]

pairs_cu = [
    ("w\т", "ot"), # vowels
    ("о_у", "u"),
    ("v'",  "i"),
    ('v"',  "i"),
    ("и",   "i"),
    ("е",   "e"),
    ("э",   "e"),
    ("jь",  "e"),
    ("ль",  "l"),  # l
    ("лi",  "li"),
    ("ля",  "la"),
    ("лe",  "le"),
    ("лю",  "lu"),
    ("л",   "7"),
    ("а",   "a"),
    ("я",   "ja"),
    ("у",   "u"),
    ("ю",   "ju"),
    ("w",   "o"),
    ("о",   "o"),
    ("=",   ""),   # diacritics
    ("'",   ""),
    ("^",   ""),
    ("`",   ""),
    ("_",   ""),
    ("ь",   ""),
    ("\ъ",  ""),
    ("Ъ",   ""),
    ("ъ",   ""),
    ("s",   "z"),  # consonants
    ("б",   "b"),
    ("ц",   "c"),
    ("д",   "d"),
    ("f",   "f"),
    ("ф",   "f"),
    ("гг",  "nh"),
    ("г",   "h"),
    ("х",   "h"),
    ("й",   "j"),
    ("к",   "k"),
    ("м",   "m"),
    ("н",   "n"),
    ("п",   "p"),
    ("р",   "r"),
    ("с",   "s"),
    ("т",   "t"),
    ("v",   "v"),
    ("в",   "v"),
    ("ы",   "i"),
    ("з",   "z"),
    ("ч",   "c"),
    ("щ",   "c"),
    ("ж",   "2"),
    ("ш",   "2"),
]

pairs_el = [
    ("ά",   "α"),  # removing accents
    ("έ",   "ε"),
    ("ή",   "η"),
    ("ί",   "ι"),
    ("ΐ",   "ϊ"),
    ("ό",   "ο"),
    ("ώ",   "ω"),
    ("ύ",   "υ"),
    ("ΰ",   "ϋ"),
    ("αι",  "e"),  # ai
    ("α",   "a"),  # alphabet
    ("β",   "v"),
    ("γ",   "h"),
    ("δ",   "d"),
    ("ε",   "e"),
    ("ζ",   "z"),
    ("η",   "i"),
    ("θ",   "f"),
    ("ι",   "i"),
    ("ϊ",   "i"),
    ("κ",   "k"),
    ("λ",   "l"),
    ("μ",   "m"),
    ("ν",   "n"),
    ("ξ",   "ks"),
    ("ο",   "o"),
    ("π",   "p"),
    ("ρ",   "r"),
    ("σ",   "s"),
    ("ς",   "s"),
    ("τ",   "t"),
    ("φ",   "f"),
    ("χ",   "h"),
    ("ψ",   "ps"),
    ("ω",   "o"),
    ("oυ",  "u"),  # handling υ
    ("aυ",  "av"),
    ("oυ",  "ov"),
    ("eυ",  "ov"),
    ("iυ",  "ov"),
    ("υi",  "hi"),
    ("υ",   "i"),
    ("ϋ",   "i"),
    ("'",   ""),
    ("’",   ""),
    ]

def metaphone_generic(pairs, word, lang='<?>'):
    original_word = word
    for (pattern, replacement) in pairs:
        word = word.replace(pattern, replacement)
    if not word:
        return '-'
    for vowel in "aeiou":
        word = word[0] + word[1:].replace(vowel, '')
    for c in word:
        if c not in metaphone_charset:
            if WARNINGS_ENABLED:
                print >> sys.stderr, ("invalid char here: %s → %s (lang: %s)"
                                      % (original_word, word, lang)).encode('utf-8')
            return '?'
    return word[:6] # cutting to 6 chars

def metaphone_pl(word):
    return metaphone_generic(pairs_pl, word, 'pl')

def metaphone_cu(word):
    word = expand_cu(word, numbers=True)
    m = re.match('[^\w]*([0-9]+)[^\w]*', word)
    if m:
        return "#" + m.group(1)
    return metaphone_generic(pairs_cu, word, 'cu')

def metaphone_el(word):
    word = simplify_el(word)
    if any(word.endswith(suffix) for suffix in ['εν', 'ον']):
        word = word[:-1]
    return metaphone_generic(pairs_el, word, 'el')

def metaphone(word, lang=None):
    word = word.lower()
    word = ignored_chars_regex.sub("", word)
    if not word:
        return '-'
    m = re.match('[^\w]*([0-9]+)[^\w]*', word)
    if m:
        return "#" + m.group(1) # a number
    if not lang:
        lang = detect_language(word)
    try:
        fun = { 'pl' : metaphone_pl,
                'cu' : metaphone_cu,
                'el' : metaphone_el }[lang]
        return fun(word)
    except KeyError:
        try:
            global WARNINGS_ENABLED
            WARNINGS_ENABLED = False
            m = metaphone_cu(word)
            if m != '?':
                return m
            m = metaphone_pl(word)
            if m != '?':
                return m
            m = metaphone_el(word)
            return m
        finally:
            WARNINGS_ENABLED = True

def detect_language(text):
    """The only diference between this function and single-word `metaphone`:
    language detection is done only once (so not on per-word basis)
    """
    for c in text: # assuming text is lowercase
        try:
            if c in "żółćęśąźń":
                return 'pl'
            name = unicodedata.name(c).split()
            if name[0] == 'CYRILLIC' or c in "~^=": # XXX = is also in titles
                return 'cu'
            if name[0] == 'GREEK':
                return 'el'
        except ValueError:
            pass
    return None


def metaphone_text(text):
    text = text.lower()
    lang = detect_language(text)
    return [metaphone(word, lang) for word in text.split()]

#def test():
#    cu_examples = [("прилjь'жнw",     "prile2no"),
#                   ("богоро'дице",    "bohorodice"),
#                   ("си^лы",          "si7y"),
#                   ("глаго'лати",     "h7aho7ati"),
#                   ("се'рдце",        "serce"),
#                   ("_о=кая'ннаго",   "okajannaho"),
#                   ("ми'лость",       "mi7ost"),
#                   ("прибjь'жище",    "pribe2ice"),
#                   ("мно'жества",     "mno2estva"),
#                   ("фараw'ня",       "faraonja"),     # ?
#                   ("бо'же'ственный", "bo2estvennij"),
#                   ("безмjь'рную",    "bezmernuju"),
#                   ("зача'ло",        "zaca7o"),
#                   ("_е=vа'ггелiе",   "evanhelje"),
#                   ("цjьлова'нiе",    "ce7ovanie"),
#                   ("соверше'нiе",    "sover2enie"),
#                   ("глагw'ланнымъ",  "h7aho7annim"),
#                   ]
#    groups = [("а='гг~лъ", "angel", "angieł"),
#              ("_Е=vа'ггелiе", "Ευαγγελίον", "Ewangelia")]
#    for value, expected in cu_examples:
#        observed = metaphone(value)
#        if observed != expected:
#            print "for input %-15s expected %-15s, got %-15s" % \
#                (value, expected, observed)
#    print 'test done.'

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
        keys = [metaphone(word) for word in line.split()]
        print " ".join(keys)
    inputFile.close()
