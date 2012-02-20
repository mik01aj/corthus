
all: $(shell ./get_make_targets.py)

HUNALIGN='/home/m01/Dropbox/corthus/poligon/hunalign-1.1/src/hunalign/hunalign'

%.pl.sentences: %.pl.txt
	./text_export.py hunalign $< pl $@
%.cu.sentences: %.cu.txt
	./text_export.py hunalign $< cu $@
%.el.sentences: %.el.txt
	./text_export.py hunalign $< el $@

%.pl-cu.hunalign: %.pl.sentences %.cu.sentences
	$(HUNALIGN) /dev/null $^ -realign -utf > $@
%.cu-el.hunalign: %.cu.sentences %.el.sentences
	$(HUNALIGN) /dev/null $^ -realign -utf > $@
%.pl-el.hunalign: %.pl.sentences %.el.sentences
	$(HUNALIGN) /dev/null $^ -realign -utf > $@
