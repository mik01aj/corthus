#!/usr/bin/python

"""
A helper script for Makefile.

Usage:
    ./get_make_targets.py <parity> <suffix>
    ./get_make_targets.py 1 .sentences  - for all possible .sentences files
    ./get_make_targets.py 2 .hunalign   - for all possible hunalign alignments
"""

import sys
import os
import re

if __name__ == '__main__':

    try:
        [parity, suffix] = sys.argv[1:]
        parity = int(parity)
        assert parity in [1,2,3], parity
    except ValueError:
        print __doc__
        sys.exit()

    texts_dir = os.path.dirname(__file__) + '/texts/'

    files = set()

    for d, ds, fs in os.walk(texts_dir):
        for f in fs:
            files.add(os.path.join(d, f))

    grouped = {}

    while files:
        filename = files.pop()
        m = re.match('(.+)/([a-z]{2}).txt$', filename)
        if m:
            basename = m.group(1)
            lang = m.group(2)
            grouped[basename] = grouped.get(basename, []) + [lang]
            if parity == 1:
                print basename + '/' + lang + suffix

    if parity == 2:
        for k, v in sorted(grouped.items()):
            if 'pl' in v and 'cu' in v:
                print k + '/pl-cu' + suffix
            if 'cu' in v and 'el' in v:
                print k + '/cu-el' + suffix
            if 'pl' in v and 'el' in v:
                print k + '/pl-el' + suffix
    elif parity == 3:
        for k, v in sorted(grouped.items()):
            if 'pl' in v and 'cu' in v and 'el' in v:
                print k + '.pl-cu-el' + suffix

