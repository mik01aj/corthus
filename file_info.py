#!/usr/bin/python

"""
Usage: ./file_info.py <files> ...
"""

import sys
import re
import os.path

def get_info(filename):

    # alignment
    m = re.match('(.*)\.(\w\w)-(\w\w).(\w+)$', filename)
    if m:
        from toolkit import Alignment
        a = Alignment.from_file(filename)
        return { 'type' : 'alignment2',
                 'basename' : m.group(1),
                 'lang1' : m.group(2),
                 'lang2' : m.group(3),
                 'text1' : "%s.%s.txt" % (m.group(1), m.group(2)),
                 'text2' : "%s.%s.txt" % (m.group(1), m.group(3)),
                 'backend' : m.group(4),
                 'cost' : a.summed_cost(),
                 'rungs' : len(a.data),
                 'filename' : filename }

    m = re.match('(.*)\.(\w\w).txt+$', filename)
    if m:
        from toolkit import Text
        t = Text.from_file(filename)
        return { 'type' : 'text',
                 'basename' : m.group(1),
                 'lang' : m.group(2),
                 'paragraphs' : len(t.as_paragraphs()),
                 'length' : len(t.as_string()),
                 'filename' : filename,
                 'title' : t.as_paragraphs()[0] }

    return { 'filename' : filename,
             'size' : os.path.getsize(filename) }


if __name__ == '__main__':
    filenames = sys.argv[1:]
    if not filenames:
        print __doc__
        sys.exit()
    for filename in filenames:
        print filename
        for k, v in sorted(get_info(filename).items()):
            print "    %-12s %s" % (k+":", unicode(v).encode('utf-8'))
