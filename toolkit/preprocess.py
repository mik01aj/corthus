#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re

from translit import metaphone_text

def preprocess(sent, use_metaphone=True):
    sent = re.sub('[¶♦\'=`^]', '', sent)
    sent = re.sub('([.,:;!?])', r' \1 ', sent)
    sent = re.sub('\s+', ' ', sent)
    if use_metaphone:
        sent = metaphone_text(sent, remove_vowels=False, max_length=20)
        sent = re.sub('\s?[-?]\s?', ' ', sent)
        sent = sent.strip()
    else:
        sent = sent.lower()
    return sent

