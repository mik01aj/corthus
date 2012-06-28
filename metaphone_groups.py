#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import defaultdict
import sys
import re

from translit.metaphone import metaphone

groups = defaultdict(lambda: set())

if __name__ == '__main__':
    for line in sys.stdin:
        for word in line.split():
            word = unicode(word, 'utf-8')
            word = re.sub("[=,.:;]", "", word.lower(), re.UNICODE)
            for key in metaphone(word):
                groups[key].add(word)

    for m, ws in groups.items():
        if len(ws) < 10:
            continue
        print (m + "\t" + " ".join(ws)).encode('utf-8')

