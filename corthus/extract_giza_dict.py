#!/usr/bin/python

"""

what I did:

from NewAlignment.py:

with open('texts/kanon_izr/everything') as f:
    a = NewAlignment.read(f)
with open('/tmp/sents_cu', 'w') as f1:
    with open('/tmp/sents_el', 'w') as f2:
        a.export_sentences_for_giza('cu', 'el', f1, f2)

./plain2snt.out /tmp/sents_cu /tmp/sents_el
./snt2cooc.out /tmp/sents_cu.vcb /tmp/sents_el.vcb /tmp/sents_cu_sents_el.snt > /tmp/cooc
./GIZA++ -S /tmp/sents_cu.vcb -T /tmp/sents_el.vcb -C /tmp/sents_cu_sents_el.snt -p0 0.98 -CoocurrenceFile /tmp/cooc -o /tmp/dict

"""

fn = '/tmp/dict'

def read_vcb(stream):
    d = {}
    for line in f:
        x, word, count = line.split()
        d[int(x)] = (word.decode('utf-8'), count)
    return d

with open(fn + '.trn.src.vcb') as f:
    d1 = read_vcb(f)

with open(fn + '.trn.trg.vcb') as f:
    d2 = read_vcb(f)

mapping = []
l = []
with open(fn + '.t3.final') as f:
    for line in f:
        x, y, p = line.split()
        x = int(x)
        y = int(y)
        p = float(p)
        mapping.append((x, y, p))
        if p > 0.5 and x > 1 and y > 1:
            l.append((p, d1[x][0], d2[y][0]))

l.sort()
l.reverse()

for p, w1, w2 in l:
    print ("%-15s %-15s %1.2f" % (w1, w2, p)).encode('utf-8')
