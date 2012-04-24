#!/usr/bin/python

"""
A helper script for Makefile.
"""

import sys
import os
import re

if __name__ == '__main__':
    texts_dir = os.path.dirname(__file__) + '/texts/'

    files = set(os.listdir(texts_dir))

    grouped = {}

    while files:
        filename = files.pop()
        m = re.match('(.+)\.([a-z]{2}).txt', filename)
        if m:
            basename = texts_dir + m.group(1)
            lang = m.group(2)
            grouped[basename] = grouped.get(basename, []) + [lang]

    for k, v in grouped.items():
        if 'pl' in v and 'cu' in v:
            print k + '.pl-cu.hunalign'
        if 'cu' in v and 'el' in v:
            print k + '.cu-el.hunalign'
        if 'pl' in v and 'el' in v:
            print k + '.pl-el.hunalign'
