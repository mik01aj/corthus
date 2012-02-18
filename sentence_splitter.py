# -*- coding: utf-8 -*-

'''
Created on Nov 16, 2011

@author: m01
'''

import re
import nltk

def split_sentences(text, lang):
    if isinstance(text, str):
        text = unicode(text, 'utf-8')
    assert isinstance(text, unicode), type(text)

    if lang == 'cu':
        return split_sentences_cu(text)
    elif lang == 'el':
        return split_sentences_el(text)
    else:
        return nltk.sent_tokenize(text)

def split_sentences_cu(text):
    '''Returns an iterator over text's sentences. It should be run on one
    paragraph - not on the whole text - because it treats first words
    specially.
    '''
    if isinstance(text, str):
        text = unicode(text, 'utf-8')
    assert isinstance(text, unicode), type(text)

    sent = []
    words = text.split()
    while True:
        change = False
        for i in range(3):
            if len(words) > i and words[i].endswith(':'):
                yield u' '.join(words[:i+1])
                words = words[i+1:]
                change = True
                break
        if not change:
            break
    for w in words:
        sent.append(w)
        if len(sent) >= 3 and re.match(ur"\S+, гла'съ \S+[:,.]$",
                                       ' '.join(sent[-3:])):
            yield ' '.join(sent[:-2])
            sent = sent[-2:]
        if any([w.endswith(u'.') and not w.endswith(u"с."),
                w.endswith(u'!'),
                w.endswith(u';'),
                re.match(ur"и= ны'нjь[:,]", u' '.join(sent[-2:])),
                ' '.join(sent[-3:]) == ur"на Гд\си воззва'хъ,"]):
            yield ' '.join(sent)
            sent = []
    if sent:
        yield ' '.join(sent)

def split_sentences_el(text):
    if isinstance(text, str):
        text = unicode(text, 'utf-8')
    assert isinstance(text, unicode), type(text)
    sent = []
    words = text.split()
    if words and words[0].endswith(':'):
        yield words[0]
        words = words[1:]
    elif len(words) > 1 and words[1].endswith(':'):
        yield u' '.join(words[:2])
        words = words[2:]
    for w in words:
        sent.append(w)
        if any([w.endswith(u'.') and not w in [u"πλ.", u"Στίχ."],
                w.endswith(u'!'),
                w.endswith(u':'),
                w.endswith(u';'),
                re.match(ur"и= ны'нjь[:,]", u' '.join(sent[-2:])),
                len(w) < 4 and len(sent) >= 2 and (sent[-2] == u"ᾨδὴ" or sent[-2] == u"Ωδή"),
                ' '.join(sent[-3:]) == ur"на Гд\си воззва'хъ,"]):
            yield ' '.join(sent)
            sent = []
    if sent:
        yield ' '.join(sent)

