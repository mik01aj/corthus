#! -*- coding: utf-8 -*-

from __future__ import unicode_literals
import textwrap
import re
import sys

class Row(object):
    def __init__(self):
        self.fragments = {}
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
        references as needed. Don't add rows manually, as this will
        break references!"""

        # updating references
        if self.rows:
            row.prev_row = self.rows[-1]
            row.prev_row.next_row = row
        for lang in row.fragments:
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
            row = Row()
            row.fragments = d
            self.append(row)

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
            row.fragments = {}
            for lang, fragment in zip(langs, fragments):

                if fragment:
                    fragment = (separator.join(fragment) + separator)
                    fragment = re.sub('\s*♦?\s*¶\s*♦\s*', ' ¶ ',
                                      fragment, re.UNICODE)
                    fragment = fragment.strip()
                    if fragment == '¶' and prev[lang]:
                        if prev[lang].fragments[lang].endswith('♦'):
                            prev[lang].fragments[lang] = \
                                prev[lang].fragments[lang][:-1] + "¶"
                        else:
                            prev[lang].fragments[lang] += " ¶"
                        continue
                    row.fragments[lang] = fragment

            if not row.fragments:
                continue

            a.append(row)

        return a

    def dump(self, stream=sys.stdout):
        for row in self.rows:
            for lang, fragment in sorted(row.fragments.items()):
                print >> stream, lang, unicode(fragment).encode('utf-8')
            print >> stream

    def pprint_text(self, lang, stream=sys.stdout, width=70):
        fragments = []
        for row in self.rows:
            if lang in row.fragments:
                fragments.append(row.fragments[lang])
        string = ''.join(fragments)
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
                    if row.fragments:
                        a.append(row)
                        row = Row()
                else:
                    assert line[2] == ' ', line
                    try:
                        row.fragments[line[0:2]] += " " + line[3:]
                    except KeyError:
                        row.fragments[line[0:2]] = line[3:]
            return a
        except Exception, e:
            raise IOError("parse error in line %d: %s" % (i, e))

    def export_sentences_for_giza(self, lang1, lang2, stream1, stream2,
                                  use_metaphone=True):
        from translit import metaphone_text
        def preprocess_sent(sent):
            sent = re.sub('[¶♦\'=`^]', '', sent)
            sent = re.sub('([.,:;!?])', r' \1 ', sent)
            sent = re.sub('\s+', ' ', sent)
            sent = sent.lower()
            if use_metaphone:
                sent = metaphone_text(sent, remove_vowels=False, max_length=20)
            return sent
        for row in self.rows:
            if lang1 in row.fragments and lang2 in row.fragments:
                sent1 = row.fragments[lang1]
                sent2 = row.fragments[lang2]
                print >> stream1, preprocess_sent(sent1).encode('utf-8')
                print >> stream2, preprocess_sent(sent2).encode('utf-8')

#    def __str__(self):
#        return '<NewAlignment>'


if __name__ == '__main__':
    import sys

    arg = sys.argv[1]

    if arg == 'export':
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
        from TextFolder import TextFolder
        pt = TextFolder(arg) # e.g. texts/kanon_izr
        langs = ['pl', 'cu', 'el']
        oa = pt.get_alignment(langs, 'my')
        seqs = [pt.get_sentences(lang) for lang in langs]
        a = NewAlignment.from_old_alignment(oa, langs, seqs)
        a.dump()
        a.pprint_text('pl')
