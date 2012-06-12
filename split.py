#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script splits files like "Ton_1.pl.txt" to parts for each day of
week, like "1_1nd.pl.txt", "1_2pn.pl.txt", depending on the
regex. Basically it's for splitting large files into smaller ones, one
for each chapter.

Usage: ./split.py [<filename> ...]   - shows preview
       ./split.py [<filename> ...] ! - does the job (and removes original)
"""

import os
import re
import sys
import subprocess

def split(filenames):
    processed_files = []
    for fn in filenames:
        m = re.match('(.*)\.([a-z]{2})\.txt$', fn)
        if not m:
            continue

        basename = m.group(1)
        lang = m.group(2)

        if lang == 'pl' and re.match('.*Tydzien_[^_]*$', basename):
            line_regex = r"W.*(wieczorem|wieczór)"
        elif lang == 'cu' and re.match(r'\dsedmpaskh|svetlaya', basename):
            line_regex = r"В.*ве'чера.*"
        else:
            continue

#        suffixes = ['1nd', '2pn', '3vt', '4sr', '5ch', '6pt', '7sb']
        suffixes = "ABCDEFGH"

        print fn
        processed_files.append(fn)

        contents = ''
        with open(fn) as f:

            dont_split_on_next_match = True
            firstline = next(f)
            line_count = 1
            matched_line_count = 0
            start_line = 0

            try:
                for suffix in suffixes:

                    if suffix=='1nd':
                        firstline = next(f)

                    start_line = line_count - 1

                    wfn = "%s_%s.%s.txt" % (basename, suffix, lang)
                    print '    %s:' % suffix

                    if basename.endswith("Paschalny"):
                        dont_split_on_next_match=False # dla tygodnia Paschalnego

                    with file('/dev/null' if DEBUG else wfn, 'w') as wf:
                        wf.write(firstline)
                        print "        line %3d: %s" % (line_count, firstline.strip())
                        firstline = 'END'
                        while True:
                            line = next(f) # this may throw StopIteration
                            line_count += 1
                            if re.match(line_regex, line):
                                matched_line_count += 1
                                if dont_split_on_next_match:
                                    print "        line %3d: %s" % (line_count, line.strip())
                                    dont_split_on_next_match = False
                                else:
                                    firstline = line
                                    break;
                            wf.write(line)

                    print '        total %d lines in %s' % (line_count - start_line, wfn)

            except StopIteration:
                print '        total %d lines' % (line_count - start_line)
                print "    EOF after %d lines" % line_count

            print "    %d matching lines found" % matched_line_count

    if not DEBUG:
        for f in processed_files:
            subprocess.call(['trash', f])
        print
        print "These files were processed and moved to trash:"
        print " ".join(processed_files)


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print __doc__
        sys.exit()
    if '!' in args:
        DEBUG = False
        args.remove('!')
    else:
        DEBUG = True
    split(args)
