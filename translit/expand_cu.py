#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script for expanding church-slavonic abbreviations, and converting
numbers to their normal form.

Usage: ./expand_cu.py <file>  (to use text file as input)
       ./expand_cu.py -       (to use standard input)
"""


from __future__ import unicode_literals

import sys
import re

pairs = [
    (r"а='гг~л",     "а='ггел"), # may cause problems
    (r"бл~г",        "бла'г"),
    (r"бл~ж",        "бла'ж"),
    (r"бл~зjь",      "бла'зjь"),
    (r"блг\д",       "блгагода'"),
    (r"блг\с",       "блгагосло'"),
    (r"бг~",         "бо'г"),
    (r"бг~ови",      "бо'гови"),
    (r"бж~",         "бо'ж"),
    (r"бз~jь",       "бо'зjь"),
    (r"бг~о",        "бого"),
    (r"бц\д",        "богоро'диц"),
    (r"бж\с",        "боже'с"),
    (r"ч~нi",        "че'ни"),
    (r"чт\с",        "че'ст"),
    (r"ч\стн",       "че'стн"),
    (r"чт\сн",       "че'стн"),
    (r"чл~в",        "челов"),
    (r"ч~н",         "чени'"),
    (r"чн~",         "чени'"),
    (r"ч\ст",        "чи'ст"),
    (r"чт~",         "чи'те"),
    (r"чт\са",       "чиста"),
    (r"чт\сот",      "чистот"),
    (r"дв~д",        "давi'д"),
    (r"дв~",         "де'в"),
    (r"дх~",         "ду'х"),
    (r"дс~",         "ду'ш"),
    (r"дш~",         "ду'ш"),
    (r"_е=п\ск",     "_е=пi'ск"),
    (r"_е=v\гл",     "_е=vа'ггел"),
    (r"_е=v\глi'",   "_е=vаггели'"),
    (r"гл~г",        "глаг"),
    (r"гл~",         "глаго'л"),
    (r"гд\с",        "го'спод"),
    (r"гд\св",       "го'сподев"),
    (r"гд\сь",       "госпо'дь"),
    (r"гд\сень",     "госпо'день"),
    (r"гд\сн",       "госпо'дн"),
    (r"гд\сс",       "госпо'дс"),
    (r"гд\си'",      "господи'"),
    (r"гп\сже`",     "госпоже`"),
    (r"хр\ст",       "хрiст"),
    (r"i=и~с",       "i=ису'с"),
    (r"i=и~лс",      "i=зра'илс"),
    (r"i=и~лт",      "i=зра'илт"),
    (r"i=ер\сл",     "i=ерусал"),
    (r"i=и~л",       "i=зраи'л"),
    (r"i=и~лi'",     "i=израили'"),
    (r"кн~",         "кня"),
    (r"кр~щ",        "кре'щ"),
    (r"кр\ст",       "крест"),
    (r"кр\стъ",      "кре'стъ"),
    (r"кр\стовоскр\с", "крестовоскре'с"),
    (r"мт~р",        "ма'тер"),
    (r"мт~и",        "ма'ти"),
    (r"мр~i",        "мари"),
    (r"мч\с",        "ме'сяч"),
    (r"мц\с",        "ме'сяц"),
    (r"мл\ст",       "ми'лост"),
    (r"мл\ср",       "милосе'р"),
    (r"мл~т",        "моли'т"),
    (r"мч~н",        "му'чен"),
    (r"мч~нч",       "му'ченич"),
    (r"м\др",        "му'др"),
    (r"нб~",         "не'б"),
    (r"нб\с",        "небе'с"),
    (r"нб~с",        "небе'с"),
    (r"нн~",         "ны'н"),
    (r"_о=ч~",       "оте'ч"),
    (r"_о='ч~",      "_о='тч"),
    (r"_о=ц~ъ",      "_о=те'ц`"),
    (r"_о=ц~",       "_о=тц"),
    (r"пл~т",        "пло'т"),
    (r"п\сл",        "по'стол"),
    (r"п\слс",       "по'столс"),
    (r"прв\д",       "пра'вед"),
    (r"пр\дт",       "предт"),
    (r"прп\д",       "преподо'"),
    (r"пр\ст",       "прест"),
    (r"пр\сн",       "при'сн"),
    (r"пр\ор",       "прор"),
    (r"рж\ст",       "рожде'ст"),
    (r"ср\дц",       "се'рдц"),
    (r"см~рт",       "сме'рт"),
    (r"сл~н",        "со'лн"),
    (r"сп~с",        "спа'с"),
    (r"стр\ст",      "стра'ст"),
    (r"сщ~",         "свящ"),
    (r"ст~",         "свят"),
    (r"ст~ъ",        "свя'тъ"),
    (r"сн~",         "сы'н"),
    (r"тр\оч",       "тро'ич"),
    (r"тр\оц",       "тро'иц"),
    (r"цр~",         "ца'р"),
    (r"цр\ств",      "ца'рств"),
    (r"цр~к",        "це'рк"),
    (r"вл\д",        "влады'"),
    (r"вл\дчц",      "влады'чиц"),
    (r"воскр~",      "воскре'"),
    (r"воскр\с",     "воскре'с"),
    (r"воскр\снiе",  "воскресе'ние"),
    (r"w=блг\дти`",  "w=благодати`"),
]

# sort pairs to have longest strings first
pairs.sort(cmp=lambda (x, x2), (y, y2): -cmp(len(x), len(y)))

def titlecase(string):
    if string:
        if string[0].isalpha():
            return string[0].upper() + string[1:]
        else: # not correct, but enough
            return string[:2].upper() + string[2:]
    else:
        return ""

def expand_cu(string, numbers=True):
    for (pattern, replacement) in pairs:
        string = string.replace(pattern, replacement)
        string = string.replace(titlecase(pattern), titlecase(replacement))
        if numbers:
            string = replace_numbers(string)
    return string


numbers_1 = ('а', 'в', 'г', 'д', '_е', 's', 'з', 'и', 'f')
numbers_10 = ('_i', 'к', 'л', 'м', 'н', '_кс', '_о', 'п', 'ч')
numbers_100 = ('р', 'с', 'т', 'ф', 'х', '_у', '_пс', 'w\т', 'ц')

def convert_number(m):
    """Converts a church-slavonic number to normal form (assuming that
    given text is really a number). Expects unicode input. Returns int.
    """
    number = 0
    for i in range(9):
        if numbers_1[i] in m: number += i+1
        if numbers_10[i] in m: number += (i+1)*10
        if numbers_100[i] in m: number += (i+1)*100
    return number

def replace_numbers(text):
    # regex syntax: (?=...)  - look ahead,
    #               (?<=...) - look behind
    #               (?:...)  - groups that will not be referenced
    #                       (--- this is what we really match    ---)
    regex = ('(?<=[-\s\.<>])((?:$C~$B?|$C~?$B~)$A?|$B~$A?|$A~(?:_i)?)(?=[-\s\.,:$%\)\]])')
    to_re = lambda l: '(%s)' % '|'.join(map(re.escape, l))
    regex = regex.replace('$A', to_re(numbers_1))
    regex = regex.replace('$B', to_re(numbers_10))
    regex = regex.replace('$C', to_re(numbers_100))
    text = " " + text + " "
    text = re.sub(regex,
                  lambda m: unicode(convert_number(m.group(0))),
                  text, re.UNICODE | re.MULTILINE)
    return text[1:-1]


if __name__ == '__main__':
    try:
        [filename] = sys.argv[1:]
        if filename == '-':
            inputFile = sys.stdin
        else:
            inputFile = open(filename)
    except ValueError:
        print __doc__
        print "Patterns replaced (in this order):"
        for (a, b) in pairs:
            print ("%20s → %s" % (a, b)).encode('utf-8')
        sys.exit()
    for line in inputFile:
        line = line[:-1].decode('utf-8') # omitting '\n'
        line = expand_cu(line)
        print line.encode('utf-8')
    inputFile.close()
