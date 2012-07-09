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
    (r"гг~л",        "ггел"), # may cause problems (ангел)
    (r"г~гл",        "ггел"),
    (r"бл~г",        "бла'г"),
    (r"бл~ж",        "бла'ж"),
    (r"бл~зjь",      "бла'зjь"),
    (r"блг\д",       "блгагода'"),
    (r"блг\с",       "блгагосло'"),
    (r"w=блг\дти`",  "w=благодати`"),
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
    (r"дв\с",        "де'вс"),
    (r"дх~",         "ду'х"),
    (r"дс~",         "ду'ш"),
    (r"дш~",         "ду'ш"),
    (r"п\ск",        "пi'ск"),       # епископ
    (r"v\гл",        "vа'ггел"),     # евангелие
    (r"v\глi'",      "vаггелi'"),
    (r"гл~г",        "глаг"),
    (r"гл~",         "глаго'л"),
    (r"гд\с",        "го'спод"),
    (r"гд\св",       "го'сподев"),
    (r"гд\сь",       "госпо'дь"),
    (r"гд\сень",     "госпо'день"),
    (r"гд\сн",       "госпо'дн"),
    (r"гд\сс",       "госпо'дс"),
    (r"гд\си'",      "господи'"),
    (r"гп\сж",       "госпож"),
    (r"хр\ст",       "хрiст"),
    (r"i=и~с",       "i=ису'с"),
    (r"iи~с",        "i=ису'с"),
    (r"i=и~лс",      "i=зра'илс"),
    (r"iи~лс",       "i=зра'илс"),
    (r"i=и~лт",      "i=зра'илт"),
    (r"iи~лт",       "i=зра'илт"),
    (r"i=ер\сл",     "i=ерусал"),
    (r"iер\сл",      "i=ерусал"),
    (r"i=и~л",       "i=зраи'л"),
    (r"iи~л",        "i=зраи'л"),
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
    (r"мл\дн",       "младе'н"),
    (r"мч~н",        "му'чен"),
    (r"мч~нч",       "му'ченич"),
    (r"м\др",        "му'др"),
    (r"нб~",         "не'б"),
    (r"нб\с",        "небе'с"),
    (r"нб~с",        "небе'с"),
    (r"нн~",         "ны'н"),
    (r"_о=ч~",       "о=те'ч"),
    (r"_оч~",        "о=те'ч"),
    (r"_о='ч~",      "_о='тч"),
    (r"_о'ч~",       "_о='тч"),
    (r"_о=ц~ъ",      "_о=те'цъ"),
    (r"_оц~ъ",       "_о=те'цъ"),
    (r"_о=ц~",       "_о=тц"),
    (r"_оц~",        "_о=тц"),
    (r"о_у=ч~тл",    "о_у=чи'тел"),
    (r"о_уч~тл",     "о_у=чи'тел"),
    (r"пл~т",        "пло'т"),
    (r"п\сл",        "по'стол"), # апостол
    (r"п\ст",        "по'ст"),
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
    (r"цр\с",        "ца'рс"),
    (r"цр~к",        "це'рк"),
    (r"вл\д",        "влады'"),
    (r"вл\дчц",      "влады'чиц"),
    (r"воскр~",      "воскре'"),
    (r"воскр\с",     "воскре'с"),
    (r"воскр\снiе",  "воскресе'ние"),
    (r"_пса\л",      "_псало'мъ"),
    (r"за\ч",        "зача'ло"),
    (r"пн\де",       "понедjь'льникъ"),
    (r"вто\р",       "вто'рникъ"),
    (r"ср\д",        "сре'д"),
    (r"че\к",        "четверто'къ"),
    (r"пя\к",        "пято'къ"),
#    (r"",        "суббw'та"),
    (r"нл\д",        "недjь'л"),
    (r"с\х",        "сти'х"),
#    (r"",        ""),
#    (r"",        ""),
]

def titlecase(string):
    if string:
        if string[0].isalpha():
            return string[0].upper() + string[1:]
        else: # not correct, but enough
            return string[:2].upper() + string[2:]
    else:
        return ""

def multi_replace(pairs, runs=1, longest_first=False, add_titlecase=False):
    """This function returns a function, which replaces strings,
    according to given pattern-replacement pairs. When matches overlap,
    it replaces only the first one. To handle overlapping matches, one
    can run this algorithm several times (use `runs` attribute)."""

    if longest_first:
        # sort pairs to have longest strings first
        pairs.sort(cmp=lambda (x, x2), (y, y2): -cmp(len(x), len(y)))

    regex = "(%s)" % '|'.join(re.escape(p[0]) for p in pairs)
    regex = re.compile(regex, re.UNICODE)

    replacements = dict(pairs)

    def run_replace(string):
        return regex.sub(lambda m: replacements[m.group(0)],
                         string)
    return run_replace

pairs.extend([(titlecase(pattern), titlecase(replacement))
              for pattern, replacement in pairs])
expand_abbreviations = multi_replace(pairs, longest_first=True, add_titlecase=True)

def expand_cu(string, numbers=True):
    string = expand_abbreviations(string)
    if numbers:
        string = replace_numbers(string)
    return string


numbers_1 = ('а', 'в', 'г', 'д', '_е', 's', 'з', 'и', 'f')
numbers_10 = ('_i', 'к', 'л', 'м', 'н', '_кс', '_о', 'п', 'ч')
numbers_100 = ('р', 'с', 'т', 'ф', 'х', '_у', '_пс', 'w\т', 'ц')
# regex syntax: (?=...) look ahead, (?<=...) look behind
#                                (____this_is_what_we_really_match_______)
number_regex = '(?<=[-\s\.<\(\[])(($C~$B?|$C?~?$B~)$A?|$C?~?$B?~?$A~(_i)?)(?=[-\s\.,:$%\)\]>])'
to_re = lambda l: '(%s)' % '|'.join(map(re.escape, l))
number_regex = number_regex.replace('$A', to_re(numbers_1))
number_regex = number_regex.replace('$B', to_re(numbers_10))
number_regex = number_regex.replace('$C', to_re(numbers_100))
del(to_re)
number_regex = re.compile(number_regex, re.UNICODE | re.MULTILINE)

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
    text = " " + text + " "
    text = number_regex.sub(lambda m: unicode(convert_number(m.group(0))),
                            text)
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
