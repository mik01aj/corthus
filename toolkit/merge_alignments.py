#!/usr/bin/python
# -*- coding: utf-8 -*-

from Text import Text
from Alignment import Alignment

def merge_3_alignments(al12, al23, al31):
    map12 = { a : b for a, b in al12 }
    map23 = { a : b for a, b in al23 }
#    map31 = { a : b for a, b in al31 }

#    print al12[:10]
#    print al23[:10]
#    print al31[:10]

    #TODO partial matches

    def gen():
        for (i1, i2) in al12:
            try:
                i3 = map23[i2]
#                if map31[i3] == i1:
                yield (i1, i2, i3)
            except KeyError:
                pass
    return Alignment(list(gen()), no_costs=True)

if __name__ == '__main__':
    import sys
    name = sys.argv[1]

    a1 = Alignment.from_file(name + '/pl-cu.my').as_ladder()
    a2 = Alignment.from_file(name + '/cu-el.my').as_ladder()
    a3 = Alignment.from_file(name + '/pl-el.my').as_ladder()
    a3 = [(b, a) for (a, b) in a3]

    ma = merge_3_alignments(a1, a2, a3)

    ma.pretty_print(Text.from_file(name + '/pl.txt', lang='pl').as_sentences_flat(),
                    Text.from_file(name + '/cu.txt', lang='cu').as_sentences_flat(),
                    Text.from_file(name + '/el.txt', lang='el').as_sentences_flat())
