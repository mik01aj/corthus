#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from preprocess import preprocess
import textwrap
import re
import sys

class Row(dict):
    def __init__(self, d=None):
        if d:
            for k, v in d.items():
                self[k] = v
        self.next = {}
        self.prev = {}
        self.next_row = None
        self.prev_row = None
        # each Row is responsible for its own prev* references, and
        # all the next* references that point to this Row

class NewAlignment(object):

    def __init__(self, data=[]):
        self.rows = list(data)
        self.prev_refs = {}

    def append(self, row):
        """This method appends a row to self.rows, updating the
        references as needed. Don't append rows manually to self.rows,
        as this will break references!"""

        # updating references
        if self.rows:
            row.prev_row = self.rows[-1]
            row.prev_row.next_row = row
        for lang in row:
            if lang in self.prev_refs:
                row.prev[lang] = self.prev_refs[lang]
                row.prev[lang].next[lang] = row
            self.prev_refs[lang] = row
        self.rows.append(row)

    def easy_append(self, **d):
        """This method also removes empty strings. Example:
        a.easy_append(pl='a', cu='b', el='')
        """
        for k in d.keys():
            d[k] = d[k].strip()
            if not d[k]:
                del d[k]
        if d:
            row = Row(d)
            self.append(row)

    @classmethod
    def from_folder(cls, path, langs=None):
        from TextFolder import TextFolder
        pt = TextFolder(path)
        if not langs:
            langs = ['pl', 'cu', 'el']
        oa = pt.get_alignment(langs, 'my')
        seqs = [pt.get_sentences(lang) for lang in langs]
        return NewAlignment.from_old_alignment(oa, langs, seqs)

    @classmethod
    def from_old_alignment(cls, alignment, langs, seqs):
        separator=' ♦ '
        a = NewAlignment()
        prev_row = None
        prev = {}
        alignment.dump('/tmp/a')
        for fragments in alignment.as_ranges(*seqs, with_costs=True):
            # fragments - one row from alignment table: [f1, f2, ..., cost]

            row = Row()
            for lang, fragment in zip(langs, fragments):

                if fragment:
                    fragment = (separator.join(fragment) + separator)
                    fragment = re.sub('\s*♦?\s*¶\s*♦\s*', ' ¶ ',
                                      fragment, re.UNICODE)
                    fragment = fragment.strip()
                    if lang in prev and fragment == '¶':
                        prev_row_with_lang = prev[lang]
                        if prev_row_with_lang[lang].endswith('♦'):
                            prev_row_with_lang[lang] = \
                                prev_row_with_lang[lang][:-1] + "¶"
                        else:
                            prev_row_with_lang[lang] += " ¶"
                        continue
                    row[lang] = fragment

            if not row:
                continue

            a.append(row)

        return a

    def dump(self, stream=sys.stdout):
        for row in self.rows:
            for lang, fragment in sorted(row.items()):
                print >> stream, lang, unicode(fragment).encode('utf-8')
            print >> stream

    def iter_fragments(self, lang):
        for row in self.rows:
            if lang in row:
                yield row[lang]

    def pprint_text(self, lang, stream=sys.stdout, width=70):
        string = ' '.join(self.iter_fragments(lang))
        paragraphs = [p.strip() for p in string.split('¶')]
        for paragraph in paragraphs:
#            paragraph = paragraph.replace('♦', '')
            for line in textwrap.wrap(paragraph, width=width):
                print >> stream, line.encode('utf-8')
            print >> stream

    @classmethod
    def read(cls, stream=sys.stdin):
        a = NewAlignment()
        row = Row()
        try:
            for i, line in enumerate(stream):
                line = line.decode('utf-8').strip()
                if not line: # empty line
                    if row:
                        a.append(row)
                        row = Row()
                else:
                    assert line[2] == ' ', line
                    try:
                        row[line[0:2]] += " " + line[3:]
                    except KeyError:
                        row[line[0:2]] = line[3:]
            return a
        except Exception, e:
            raise IOError("parse error in line %d: %s" % (i, e))

    def export_sentences_for_giza(self, lang1, lang2, stream1, stream2,
                                  use_metaphone=True):
        for row in self.rows:
            if lang1 in row and lang2 in row:
                print >> stream1, \
                    preprocess(row[lang1], use_metaphone).encode('utf-8')
                print >> stream2, \
                    preprocess(row[lang2], use_metaphone).encode('utf-8')

    def to_old_alignment(self, *langs):

        def iter_sents(t):
            t = t.replace('¶', '♦¶♦')
            t = t.split('♦')
            for s in t:
                s = s.strip()
                if s:
                    yield s

        a = []
        ts = tuple([] for lang in langs)

        # using convention from Haskell:
        # ts - sequence of t-s
        # ss - sequence of s-es
        # sss - sequence of ss-es

        a.append([len(t) for t in ts] + [0])

        for row in self.rows:
            something = False
            all_p = True
            for t, lang in zip(ts, langs):
                ss = list(iter_sents(row.get(lang, '')))
                if ss:
                    something = True
                t.extend(ss)
                if not ss or ss[-1] != '¶':
                    all_p = False
            if not something:
                continue
            if all_p:
                a.append([len(t)-1 for t in ts] + [0])
            a.append([len(t) for t in ts] + [0])

        from Alignment import Alignment
        return (Alignment(a), ts)

    def iter_tuples(self, *langs):
        for row in self.rows:
            yield tuple(row.get(lang, '') for lang in langs)

    def __iter__(self):
        if not self.rows:
            raise StopIteration
        r = self.rows[0]
        while True:
            yield r
            r = r.next_row
            if not r:
                raise StopIteration

    def pretty_print(self, *langs):
        assert langs
        from textwrap import wrap
        from itertools import izip_longest
        for row in self.rows:
            lines = []
            for lang in langs:
                lines.append(wrap(row.get(lang, ''), 35))
            if all(not col for col in lines):
                continue
            for output_row in izip_longest(*lines):
                # one output_row = one line of output
#                output_row = list(output_row)
                output_row = [(col if col else '')
                              for col in output_row]
                s = "|".join("%-35s%s " % (col, ' '*col.count('\u0331'))
                             for col in output_row)
                print s.encode('utf-8') # a workaround for `less`
            print


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('action', choices=['sentences', 'giza', 'dump', 'print', 'json'])
    parser.add_argument('--folder', help='')
    parser.add_argument('langs', help='langs (for all actions except giza)', type=lambda s: s.split(','))
    options = parser.parse_args()

    if options.action == 'sentences':
        fn = 'texts/kanon_izr/everything'
        out = '/tmp/'
        print 'exporting %s to %s' % (fn, out)
        with open(fn) as f:
            a = NewAlignment.read(f)
        (oa, ts) = a.to_old_alignment(*options.langs)
        oa.dump(out + '%s.new' % ('-'.join(options.langs)))
        for lang, t in zip(options.langs, ts):
            with open('/tmp/%s.sentences' % lang, 'w') as f:
                for s in t:
                    print >> f, s.encode('utf-8')
        print 'done.'

    elif options.action == 'giza':
        with open('texts/kanon_izr/everything') as f:
            a = NewAlignment.read(f)
        with open('texts/evangelie/matfea/everything') as f:
            a2 = NewAlignment.read(f)

        #a.dump()
        with open('/tmp/sents_cu', 'w') as f1:
            with open('/tmp/sents_el', 'w') as f2:
                a.export_sentences_for_giza('cu', 'el', f1, f2,
                                            use_metaphone=True)
                a2.export_sentences_for_giza('cu', 'el', f1, f2,
                                             use_metaphone=True)
    else:
        a = NewAlignment.from_folder(options.folder, options.langs) # e.g. texts/kanon_izr

        if options.action == 'dump':
            a.dump()
        elif options.action == 'print':
            a.pprint_text('pl')
        elif options.action == 'json':
            import json
            obj = {'rungs': a.rows, 'langs': options.langs}
            print json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8')
