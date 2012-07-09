
SHELL := /bin/bash
H := $(shell if [ -f /usr/local/bin/h ]; then echo h; fi)

all: sentences hunalign pairs my

# Hunalign 1.1 binary
#HUNALIGN='/home/m01/Dropbox/corthus/poligon/hunalign-1.1/src/hunalign/hunalign'
HUNALIGN='/home/d/dadela/hunalign-1.1/src/hunalign/hunalign'

sentences: $(shell ./get_make_targets.py 1 .sentences)
%.pl.sentences: %.pl.txt toolkit/sentence_splitter.py toolkit/text_export.py
	./toolkit/text_export.py hunalign $< pl > $@
%.cu.sentences: %.cu.txt toolkit/sentence_splitter.py toolkit/text_export.py
	./toolkit/text_export.py hunalign $< cu > $@
%.el.sentences: %.el.txt toolkit/sentence_splitter.py toolkit/text_export.py
	./toolkit/text_export.py hunalign $< el > $@
clean-sentences:
	find texts/ -name '*.??.sentences' -delete

hunalign: $(shell ./get_make_targets.py 2 .hunalign)
# NOTE: when translate.txt is not there, it means a Hunalign error.
# hunalign will not fail in this case, however rm will do.
%.pl-cu.hunalign: %.pl.sentences %.cu.sentences
	$(HUNALIGN) /dev/null $^ -realign -utf > $@ 2> >(tee "/tmp/$(shell echo $@.log | sed -e 's#/#_#g')" | grep Quality >&2)
#	rm translate.txt || rm $@ && cat /tmp/$(shell echo $@.log | sed -e 's#/#_#g') && false
%.cu-el.hunalign: %.cu.sentences %.el.sentences
	$(HUNALIGN) /dev/null $^ -realign -utf > $@ 2> >(tee "/tmp/$(shell echo $@.log | sed -e 's#/#_#g')" | grep Quality >&2)
#	rm translate.txt || rm $@ && cat /tmp/$(shell echo $@.log | sed -e 's#/#_#g') && false
%.pl-el.hunalign: %.pl.sentences %.el.sentences
	$(HUNALIGN) /dev/null $^ -realign -utf > $@ 2> >(tee "/tmp/$(shell echo $@.log | sed -e 's#/#_#g')" | grep Quality >&2)
#	rm translate.txt || rm $@ && cat /tmp/$(shell echo $@.log | sed -e 's#/#_#g') && false
clean-hunalign:
	find texts/ -name '*.??-??.hunalign' -delete
	rm -f /tmp/*.hunalign.log

pairs: data/pairs.pl-cu data/pairs.cu-el data/pairs.pl-el
# To require alignments, add $(shell find texts/ -name '*.??-??.hunalign') as requirement
# I'm using a wildcard here (instead of get_make_targets) because not all alignments are needed
data/pairs.pl-cu: alignment_analysis.py
	./alignment_analysis.py `find texts/ -name '*.pl-cu.hunalign'` > $@
data/pairs.cu-el: alignment_analysis.py
	./alignment_analysis.py `find texts/ -name '*.cu-el.hunalign'` > $@
data/pairs.pl-el: alignment_analysis.py
	./alignment_analysis.py `find texts/ -name '*.pl-el.hunalign'` > $@

my: $(shell ./get_make_targets.py 2 .my)
%.pl-cu.my: %.pl.sentences %.cu.sentences
	./aligner.py $^ > $@
%.cu-el.my: %.cu.sentences %.el.sentences
	./aligner.py $^ > $@
%.pl-el.my: %.pl.sentences %.el.sentences
	./aligner.py $^ > $@
clean-my:
	find texts/ -name '*.??-??.my' -delete


align3: $(shell ./get_make_targets.py 3 .3)
#TODO
clean-3:
	find texts/ -name '*.??-??-??.3' -delete; \



.PHONY: clean-hunalign clean-my clean-sentences clean-3
