
import sys
import os.path

from Text import Text
from Alignment import Alignment
import aligner
from merge_alignments import merge_3_alignments

possible_backends = ['my', 'hunalign', 'hand']
log = sys.stderr

class TextFolder:

    def __init__(self, path):
        if path.endswith('/'):
            path = path[:-1]
        assert os.path.isdir(path)
        self.path = os.path.abspath(path)
        self.name = os.path.basename(path)

    def get_text(self, lang):
        return Text.from_file(self._p(str(lang) + ".txt"), lang=str(lang))

    def get_alignment(self, langs, backend=None):
        """like fetcher"""
        assert len(langs) >= 2
        assert not backend or backend in possible_backends

        real_langs = list(set(lang[:2]
                              for lang in langs))

        if len(real_langs) == 1:
            text_len = len(fetch_sentences(basename, real_langs[0]))
            return Alignment.create_straight(text_len, len(langs))
        elif len(real_langs) == 2:
            a = None
            for i in range(2):
                for b in ([backend] if backend else possible_backends):
                    try:
                        langs_string = '-'.join(str(l) for l in real_langs)
                        a = Alignment.from_file(self._p(langs_string + '.' + b))
                        break
                    except IOError:
                        continue
                if a:
                    break
                real_langs.reverse()
            if not a:
                raise IOError

        else: # len(real_langs) == 3 :(
            a1 = self.get_alignment(['pl', 'cu'], backend).as_ladder()
            a2 = self.get_alignment(['cu', 'el'], backend).as_ladder()
            a3 = self.get_alignment(['pl', 'el'], backend).as_ladder()
#            a3 = [(b, a) for (a, b) in a3] # reversed
            a = merge_3_alignments(a1, a2, a3)
            real_langs = ['pl', 'cu', 'el'] # needed later

        columns = _transpose(a.data)
        columns_map = { real_langs[i] : columns[i]
                        for i in range(len(real_langs)) }

        # common part for 2 and 3
        chosen_columns = [columns_map[lang[:2]] for lang in langs]
        chosen_columns.append(columns[2])
        return Alignment(_transpose(chosen_columns))

    def get_sentences(self, lang):
        with open(self._p(str(lang) + '.sentences')) as f:
            return [line.strip().decode('utf-8') for line in f]

    def show(self, langs):
        """pretty-prints a text or alignment."""
        if len(langs) == 1:
            self.get_text(langs[0]).pretty_print()
        else:
            a = self.get_alignment(langs)
            a.pretty_print(*[self.get_sentences(l) for l in langs])

    def update(self):
        """check dates and do all the work necessary"""
        dependencies = []
        dependencies.append(('l.txt', l+'.sentences'))
        raise BlaBlaError

    def align(self, lang1, lang2, no_hand=False):
        seq1 = self.get_sentences(lang1)
        seq2 = self.get_sentences(lang2)
        if no_hand:
            a = aligner.align(seq1, seq2)
        else:
            hand_alignment = self.get_alignment([lang1, lang2]).as_ladder(with_costs=False)
            print >> log, "%d hand-aligned pairs found." % len(hand_alignment)
            a = aligner.make_composed_alignment(seq1, seq2, hand_alignment)
        output_filename = self._p('%s-%s.my' % (lang1, lang2))
        Alignment(a).dump(output_filename)
        print >> log, "Wrote %s." % output_filename
        return a

    def merge(self, ls1, ls2):
        """Merge 2 alignments into one, 3-way"""
        pass

    def export(self, l, format):
        pass

    def info(self):
        r = {}
        r['files'] = os.listdir(self.path)
        return r

    def status(self):
        pass

    def _p(self, filename):
        return os.path.join(self.path, filename)

    def file(self, filename, **kwargs):
        return file(self._p(filename), **kwargs)

def _transpose(arr):
    return zip(*arr)
