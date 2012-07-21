# -*- coding: utf-8 -*-

"""
Created on Nov 16, 2011
@author: m01

Sentence splitting for all languages (pl, cu, el). To use it on the
command-line, see text_export.py (export for hunalign).
"""

import re

def split_sentences(text, lang):
    if isinstance(text, str):
        text = unicode(text, 'utf-8')
    assert isinstance(text, unicode), type(text)

    if lang == 'cu':
        return split_sentences_cu(text)
    elif lang == 'el':
        return split_sentences_el(text)
    else:
        return split_sentences_pl(text)
        #TODO write something that will work without nltk
#        import nltk
#        return nltk.sent_tokenize(text)


def split_sentences_cu(text):
    """Returns an iterator over text's sentences. It should be run on one
    paragraph - not on the whole text - because it treats first words
    specially.
    """
    if isinstance(text, str):
        text = unicode(text, 'utf-8')
    assert isinstance(text, unicode), type(text)

    split_char = unicode('♦', 'utf-8')

    # 1: space or beginning
    # 2: common abbreviations (we don't match them)
    # 3: word with dot (note: \w contains, among others, cyrylic letters and underscore)
    # 4: the dot or semicolon
    # 5: optional closing brackets
    # 6: beginning of the next word (after space)
    #               (   1____    2_______ 3____________ 4_ 5______) (6__)
    text = re.sub(r"((?:\s|\A)(?!с\.|ст\.)[\w'=`~\\^-]+[.;][\]\)]?) (\w+)".decode('utf-8'),
                  r'\1' + split_char + r'\2',
                  text, flags=re.UNICODE)

    def split_if_uppercase(m):
        first_letter = m.group(2).replace("_", "")[0]
        if not first_letter or first_letter.isupper():
            return m.group(1) + split_char + m.group(2)
        else:
            return m.group(0) # no change
    text = re.sub(r"([\w'=`~\\^-]+[:!]) (\w+)",
                  split_if_uppercase,
                  text, flags=re.UNICODE)

    return text.split(split_char)


def split_sentences_pl(text):
    """Returns an iterator over text's sentences. It should be run on one
    paragraph - not on the whole text - because it treats first words
    specially.
    """
    if isinstance(text, str):
        text = unicode(text, 'utf-8')
    assert isinstance(text, unicode), type(text)

    split_char = unicode('♦', 'utf-8')

    # 1: space or beginning
    # 3: word with dot (note: \w contains, among others, Polish letters and underscore)
    # 4: the dot or semicolon
    # 5: optional closing brackets
    # 6: beginning of the next word (after space)
    #               (   1____ 3_____ 4_ 5______) (6__)
    text = re.sub(r"((?:\s|\A)[\w-]+[.;][\]\)]?) (\w+)".decode('utf-8'),
                  r'\1' + split_char + r'\2',
                  text, flags=re.UNICODE)

    def split_if_uppercase(m):
        first_letter = m.group(2).replace("_", "")[0]
        if not first_letter or first_letter.isupper():
            return m.group(1) + split_char + m.group(2)
        else:
            return m.group(0) # no change
    text = re.sub(r"([\w'=`~\\^-]+[:!?]) (\w+)",
                  split_if_uppercase,
                  text, flags=re.UNICODE)

    return text.split(split_char)


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

