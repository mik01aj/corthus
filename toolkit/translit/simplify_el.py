#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script that simplifies makes Greek text to use only one accent type
(tonos ´), and removes all diacritics, except for dialytika (¨).

Output alphabet: αά β γ δ εέ ζ ηή θ ιίϊΐ κ λ μ ν ξ οό π ρ σς τ υύϋΰ φ χ ψ ωώ
Interpunction:   ΄·.:;
(not guaranteed)

Usage: ./simplify_el.py <file>  (to use text file as input)
       ./simplify_el.py -       (to use standard input)
"""

from __future__ import unicode_literals

import sys
import unicodedata

#
# output_charset = "ςεέρτυύθιίϊοόπαάσδφγηήξκλζχψωώβνμ"
#

def simplify_el(string):
    result = []
    for c in string:
        try:
            name = unicodedata.name(c).split()
        except ValueError:
            continue
        if 'WITH' in name:
            assert name[4] == 'WITH'
            # possible diacritics: TONOS OXIA DIALYTIKA VARIA DASIA
            #                      PERISPOMENI PROSGEGRAMMENI YPOGEGRAMMENI
            diacritics = []
            if 'DIALYTIKA' in name[5:]:
                diacritics.append('DIALYTIKA')
            if any(a in name[5:]
                   for a in ['TONOS', 'OXIA', 'VARIA', 'PERISPOMENI']):
                diacritics.append('TONOS')
            new_name = name[:4]
            if len(diacritics) >= 1:
                new_name += ['WITH', diacritics[0]]
            for d in diacritics[1:]:
                new_name += ['AND', d]
            result.append(unicodedata.lookup(' '.join(new_name)))
        else:
            result.append(c)
    return ''.join(result)


#TODO: convert Greek numbers, α' β' γ' δ' ε' στ' ζ' θ' - also with ’


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
        line = simplify_el(line)
        print line
    inputFile.close()
