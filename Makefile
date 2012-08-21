
SHELL := /bin/bash
H := $(shell if [ -f ./external/hilite ]; then echo ./external/hilite; fi)

all: sentences hunalign pairs my

# Hunalign 1.1 binary
#HUNALIGN='/home/m01/Dropbox/corthus/poligon/hunalign-1.1/src/hunalign/hunalign'
#HUNALIGN='/home/d/dadela/hunalign-1.1/src/hunalign/hunalign'
HUNALIGN='./external/hunalign-1.1/src/hunalign/hunalign'

sentences: $(shell ./get_make_targets.py 1 .sentences)
%.pl.sentences: %.pl.txt toolkit/sentence_splitter.py toolkit/text_export.py
	$(H) ./toolkit/text_export.py sentences$< pl > $@
%.cu.sentences: %.cu.txt toolkit/sentence_splitter.py toolkit/text_export.py
	$(H) ./toolkit/text_export.py sentences$< cu > $@
%.el.sentences: %.el.txt toolkit/sentence_splitter.py toolkit/text_export.py
	$(H) ./toolkit/text_export.py sentences$< el > $@
clean-sentences:
	find texts/ -name '*.??.sentences' -delete

huninput: $(shell ./get_make_targets.py 1 .huninput)
%.pl.huninput: %.pl.txt toolkit/sentence_splitter.py toolkit/text_export.py
	$(H) ./toolkit/text_export.py hunalign $< pl > $@
%.cu.huninput: %.cu.txt toolkit/sentence_splitter.py toolkit/text_export.py
	$(H) ./toolkit/text_export.py hunalign $< cu > $@
%.el.huninput: %.el.txt toolkit/sentence_splitter.py toolkit/text_export.py
	$(H) ./toolkit/text_export.py hunalign $< el > $@
clean-huninput:
	find texts/ -name '*.??.huninput' -delete

hunalign: $(shell ./get_make_targets.py 2 .hunalign)
# NOTE: when translate.txt is not there, it means a Hunalign error.
# hunalign will not fail in this case, however rm will do.
%.pl-cu.hunalign: %.pl.huninput %.cu.huninput
	$(HUNALIGN) /dev/null $^ -realign -utf > $@ 2> >(tee "/tmp/$(shell echo $@.log | sed -e 's#/#_#g')" | grep Quality >&2)
#	rm translate.txt || rm $@ && cat /tmp/$(shell echo $@.log | sed -e 's#/#_#g') && false
%.cu-el.hunalign: %.cu.huninput %.el.huninput
	$(HUNALIGN) /dev/null $^ -realign -utf > $@ 2> >(tee "/tmp/$(shell echo $@.log | sed -e 's#/#_#g')" | grep Quality >&2)
#	rm translate.txt || rm $@ && cat /tmp/$(shell echo $@.log | sed -e 's#/#_#g') && false
%.pl-el.hunalign: %.pl.huninput %.el.huninput
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
%.pl-cu.my: %.pl.huninput %.cu.huninput
	./aligner.py $^ > $@
%.cu-el.my: %.cu.huninput %.el.huninput
	./aligner.py $^ > $@
%.pl-el.my: %.pl.huninput %.el.huninput
	./aligner.py $^ > $@
clean-my:
	find texts/ -name '*.??-??.my' -delete


align3: $(shell ./get_make_targets.py 3 .3)
#TODO
clean-3:
	find texts/ -name '*.??-??-??.3' -delete; \

test:
#	$(HUNALIGN) /dev/null test_data/kanon_izr.pl.metaphone test_data/kanon_izr.cu.metaphone -realign > test_data/kanon_izr.pl-cu.hunalign
	./toolkit/aligner.py test_data/kanon_izr.pl.metaphone test_data/kanon_izr.cu.metaphone > test_data/kanon_izr.pl-cu.my
	diff test_data/kanon_izr.pl-cu.golden test_data/kanon_izr.pl-cu.my

.PHONY: clean-hunalign clean-my clean-sentences clean-huninput clean-3 test
