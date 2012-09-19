#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division

import re
from toolkit.TextFolder import TextFolder
from collections import defaultdict

pt = TextFolder('texts/evangelie/matfea/')
langs = ['pl', 'cu', 'el']
#oa = pt.get_alignment(langs, 'my')
#seqs = [pt.get_sentences(lang) for lang in langs]

verses_pl = defaultdict(lambda: "")
with pt.file('pl.txt') as f:
    chapter_num = 0
    for line_num, line in enumerate(f):
        line = line.decode('utf-8').strip()
        if not line:
            continue

        if line_num == 0:
            verses_pl[0, 0] = line
            continue

        m = re.match('==([A-Za-z]+) (\d+)==$', line)
        if m:
            chapter_num = int(m.group(2))
            verses_pl[chapter_num, 0] = "Rozdział " + unicode(chapter_num)
            continue

        m = re.match('(\d+) (.+)$', line)
        if m:
            verses_pl[chapter_num, int(m.group(1))] = m.group(2)
            continue

        assert False
verses_pl.default_factory = None


from toolkit.translit.expand_cu import replace_numbers
verses_cu = defaultdict(lambda: "")
with pt.file('cu.txt') as f:
    text = '\n'.join(line.decode('utf-8').strip() for line in f)
    paragraphs = text.split('\n\n')
    chapter_num = 0
    verse_num = 0
    for paragraph in paragraphs:
        paragraph = paragraph.replace('\n', ' ')

        # removing comments
        paragraph = re.sub(r'{[^}]+}', '', paragraph, re.UNICODE)
        paragraph = re.sub(r'\([^)]+\)', '', paragraph, re.UNICODE)
        paragraph = re.sub(r'\[[^\]]+\]', '', paragraph, re.UNICODE)
        paragraph = re.sub(r'[*@]', '', paragraph, re.UNICODE)

        m = re.match('Глава` (.+)\.$', paragraph)
        if m:
            chapter_num = int(replace_numbers(m.group(1)))
            verse_num = 0
            verses_cu[chapter_num, verse_num] += paragraph
            continue # next paragraph

        words = []
        found_number_in_this_paragraph = False
        for word in paragraph.split():
            number = replace_numbers(word)
            if re.match('\d+$', number) and int(number) in [verse_num, verse_num+1, verse_num+2, verse_num+3]:
                if int(number) != verse_num + 1:
                    print chapter_num, verse_num, int(number)
                    print paragraph
                    raise SystemExit
                found_number_in_this_paragraph = True
                if words:
                    verses_cu[chapter_num, verse_num] += ' '.join(words) + ' '
                    words = []
                verse_num = int(number)
                continue # next word

            words.append(word)

        if words and found_number_in_this_paragraph:
            verses_cu[chapter_num, verse_num] += ' '.join(words) + ' '
verses_cu.default_factory = None


verses_el = defaultdict(lambda: "")
with pt.file('el.txt') as f:
    chapter_num = 0
    for line_num, line in enumerate(f):
        line = line.decode('utf-8').strip()
        if not line:
            continue

        if line_num == 0:
            verses_el[0, 0] = line
            continue

        m = re.match('==(.+)==$', line)
        if m:
            chapter_num += 1
            verses_el[chapter_num, 0] = "Κεφάλαιο " + m.group(1)
            continue

        m = re.match('{{κ\|(\d+)}} (.+)$', line)
        if m:
            verses_el[chapter_num, int(m.group(1))] = m.group(2)
            continue

        assert False, (line_num, line)
verses_el.default_factory = None


from toolkit.NewAlignment import NewAlignment

a = NewAlignment()

all_keys = sorted(set(verses_pl.keys() + verses_cu.keys()))
for ch, v in all_keys:
    s1 = verses_pl.get((ch, v), '')
    s2 = verses_cu.get((ch, v), '')
    s3 = verses_el.get((ch, v), '')

    a.easy_append(pl=s1, cu=s2, el=s3)

a.dump()

#    try:
#        ratio = (len(s1)/len(s2) + len(s2)/len(s3) + len(s3)/len(s1)) / 3
#    except ZeroDivisionError:
#        ratio = 0
#    print ("%3d %3d | %-40s %-4d | %-40s %-4d | %-40s %-4d | %1.2f %s" %
#           (ch, v,
#            s1[:40], len(s1),
#            s2[:40], len(s2),
#            s3[:40], len(s3),
#            ratio,
#            '*' if ratio > 1.3 or ratio < 0.7 else '')
#           ).encode('utf-8')

#a = NewAlignment.from_old_alignment(oa, langs, seqs)
#a.dump()

#a = NewAlignment.from_old_alignment(oa, langs, seqs)
#a.dump()
#a.pprint_text('pl')
