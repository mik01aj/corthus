#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import defaultdict
import sys
import re

from toolkit.translit.metaphone import metaphone, ignored_chars, metaphone_text

groups = defaultdict(lambda: set())

if __name__ == '__main__':
    ignored_chars_regex = re.compile("["+re.escape(ignored_chars)+"]", re.UNICODE)
    for line in sys.stdin:
##        line = line.decode('utf-8').strip()
##        groups[metaphone_text(line)].add(line)
        for word in line.split():
            word = unicode(word, 'utf-8')
            word = ignored_chars_regex.sub("", word.lower())
            groups[metaphone(word)].add(word)

    for m, ws in sorted(groups.items()):
        if len(ws) < 5:
            continue
        print (m + "\t" + " ".join(ws)).encode('utf-8')
##        print m.encode('utf-8')
##        for w in ws:
##            print '   ' + w.encode('utf-8')

