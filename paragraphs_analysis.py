#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script finds repeated paragraphs. It prints their beginnings,
together with their counts.
"""

import sys
from toolkit import Text
from collections import defaultdict

if __name__ == '__main__':

    paragraph_counts = defaultdict(lambda: 0)

    filenames = sys.argv[1:]
    for filename in filenames:
        t = Text.from_file(filename)
        for paragraph in t.as_paragraphs():
            paragraph_counts[paragraph] += 1

    paragraphs_as_list = [(count, paragraph)
                          for (paragraph, count)
                          in paragraph_counts.iteritems()]

    paragraphs_as_list.sort(reverse=True)

    for (count, paragraph) in paragraphs_as_list:
        if count > 1:
            print count, paragraph[:100].encode('utf-8')


