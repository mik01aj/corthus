
all: $(shell ./get_make_targets.py)

# Hunalign 1.1 binary
HUNALIGN='/home/m01/Dropbox/corthus/poligon/hunalign-1.1/src/hunalign/hunalign'

%.pl.sentences: %.pl.txt toolkit/sentence_splitter.py toolkit/text_export.py
	./toolkit/text_export.py hunalign $< pl $@
%.cu.sentences: %.cu.txt toolkit/sentence_splitter.py toolkit/text_export.py
	./toolkit/text_export.py hunalign $< cu $@
%.el.sentences: %.el.txt toolkit/sentence_splitter.py toolkit/text_export.py
	./toolkit/text_export.py hunalign $< el $@

%.pl-cu.hunalign: %.pl.sentences %.cu.sentences
	$(HUNALIGN) /dev/null $^ -realign -utf > $@ 2> $@.log
%.cu-el.hunalign: %.cu.sentences %.el.sentences
	$(HUNALIGN) /dev/null $^ -realign -utf > $@ 2> $@.log
%.pl-el.hunalign: %.pl.sentences %.el.sentences
	$(HUNALIGN) /dev/null $^ -realign -utf > $@ 2> $@.log

pairs: data/pairs.pl-cu data/pairs.cu-el data/pairs.pl-el
data/pairs.pl-cu: alignment_analysis.py
	./alignment_analysis.py `find texts/ -name '*.pl-cu.hunalign'` > $@
data/pairs.cu-el: alignment_analysis.py
	./alignment_analysis.py `find texts/ -name '*.cu-el.hunalign'` > $@
data/pairs.pl-el: alignment_analysis.py
	./alignment_analysis.py `find texts/ -name '*.pl-el.hunalign'` > $@
