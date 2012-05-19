#!/usr/bin/python
# -*- coding: utf-8 -*-

from toolkit import Text
import sys

def parse(text):
    """Returns a list of tuples: (tag, p) or (tag, p_1, ..., p_n)
    """
    assert isinstance(text, Text)

    iterator = iter(text.as_paragraphs())
    while True:
        paragraph = next(iterator) # StopIteration exception will be propagated
        tropar_labels = [unicode("Бг~оро'диченъ:", 'utf-8'),
                         unicode("Мч~нченъ:", 'utf-8'),
                         unicode("I=рмо'съ:", 'utf-8')]
        if any(paragraph.startswith(l) for l in tropar_labels):
            if len(paragraph) > 30:
                yield ('tropar', paragraph)
            else:
                yield ('tropar', paragraph, next(iterator))
        else:
            yield ('text', paragraph)

def _find_indices(sequence, predicate):
    """Yields all items satisying the given predicate, together with
    their indices in the sequence"""
    for i, x in enumerate(sequence):
        if predicate(x):
            yield i

def preprocess(text):
    assert isinstance(text, Text)

    def f():
        paragraph = ""
        for p in text.as_paragraphs():
            paragraph += p
            if p == unicode("И='нъ", 'utf-8'):
                paragraph += " "
            else:
                yield paragraph
                paragraph = ""
    return Text(tuple(f()))


def parse_kanon(text):
    assert isinstance(text, Text)

    paragraphs = text.as_paragraphs()

    odes = _find_indices(text.as_paragraphs(),
                         lambda p: p.startswith(unicode("Пjь'снь", 'utf-8')))
    odes = list(odes)[:8]

    ode_numbers = ["а~", "г~", "д~", "_е~", "s~", "з~", "и~", "f~"]

    def read_tropars(paragraphs, endword=None):
        for p in paragraphs:
            if p.startswith(endword):
                break
            yield p

    ode_contents = []
    for i in range(7):
        ode_contents.append(paragraphs[odes[i]:odes[i+1]])

    max_ode_tropars = max(len(x) for x in ode_contents)
    ode_contents.append(read_tropars(paragraphs[odes[7]:odes[7]+max_ode_tropars],
                                     unicode("Та'же,", 'utf-8')))

    for xs in ode_contents:
        yield xs

# Та'же, Досто'йно _е='сть:

if __name__ == '__main__':
    filename = sys.argv[1]
    for r in parse_kanon(preprocess(Text.from_file(filename))):
        print
        for x in r:
            print x[:70], ("[%d]" % len(x) if len(x) > 70 else '')

