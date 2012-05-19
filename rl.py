#!/usr/bin/python

import readline
import sys
from toolkit import Text
from textwrap import wrap

_completions_list = []

def complete(text, state):
    global _completions_list
    if state == 0:
        _completions_list = [text + "@"]
    if state < len(_completions_list):
        return _completions_list[state]
    return None

readline.read_init_file()
readline.parse_and_bind("TAB: history-search-backward")
readline.parse_and_bind("ESC: kill-line")
readline.set_completer(complete)

[filename] = sys.argv[1:]

text = Text.from_file(filename)

def tag_text(text):
    for paragraph in text.as_paragraphs():
        for l in wrap(paragraph):
            print l
        tag = raw_input()
        yield tag, paragraph

with open(filename + '.tagged', 'w') as f:
    for tag, paragraph in tag_text(text):
        lines = ["# " + tag] + wrap(paragraph) + ['']
        lines = [(l+'\n').encode('utf-8') for l in lines]
        f.writelines(lines)
