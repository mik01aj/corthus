# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import codecs
import textwrap
from sentence_splitter import split_sentences
from StringIO import StringIO

class Text(object):
    """A class that makes text available in various formats.  It is
    pretty lightweight, so it can be used just to read paragraphs of
    text from a file. All text data is stored internally as unicode
    strings.
    """

    def __init__(self, data, lang=None, coding='utf-8', name=None):
        """Create a string from given data.
        data: a string, stream (e.g. an open file), or a list of strings (paragraphs)
        """
        assert lang==None or (isinstance(lang, (unicode, str)) and len(lang)==2)
        if isinstance(data, (str, unicode)):
            # constructing a Text from a string
            self.paragraphs = tuple(_read_paragraphs(StringIO(data), coding))
        elif isinstance(data, (list, tuple)):
            # constructing a Text from a list of paragraphs
            assert all(isinstance(p, (str, unicode)) for p in data)
            self.paragraphs = tuple(data)
        else:
            # constructing a Text from a stream (e.g. an open file)
            self.paragraphs = tuple(_read_paragraphs(data, coding))

        self.lang = lang
        self.name = name

        if not self.lang:
            import sys
            print >> sys.stderr, "No lang specified for " + str(self)

    @classmethod
    def from_file(cls, file_path, *args, **kwargs):
        with codecs.open(file_path, encoding=kwargs.get('coding', 'utf-8')) as f:
            return Text(f, *args, **kwargs)

    def dump(self, file_path):
        """Write text to file, as UTF-8 plain text file, wrapped to 80
        chars per line, and "\n\n" separating the paragraphs.
        """
        with open(file_path, 'w') as f:
            _write_paragraphs(self.paragraphs, f)

    def as_string(self):
        stream = StringIO()
        _write_paragraphs(self.paragraphs, stream)
        return stream.getvalue()

    def as_paragraphs(self):
        return self.paragraphs

    def as_sentences(self, paragraph_separator=None):
        def gen():
            for p in self.paragraphs:
                for sent in split_sentences(p, self.lang):
                    yield sent
                if paragraph_separator:
                    yield paragraph_separator
        return list(gen())

    def as_sentences_flat(self):
        return self.as_sentences(paragraph_separator='¶')

    def as_sentences_nested(self):
        return [ split_sentences(p, self.lang)
                 for p in self.paragraphs ]

    # maybe also as words?

    def __str__(self):
        return ('Text:"%s..."' % self.paragraphs[0][:20]).encode('utf-8')

def _read_paragraphs(stream, coding='utf-8'):
    '''A generator to read a stream by paragraphs (separated by "\n\n").
    Stream should give a line on each iteration.
    '''
    paragraph = ''
    for line in stream:
        #assert line.endswith('\n') # not true only if file donsn't end with \n
        line = line.strip()
        if line == '' and paragraph != '':
            yield paragraph[:-1] # removing last char (space)
            paragraph = ''
        elif line != '':
            paragraph += line + ' '
    if paragraph != '':
        yield paragraph

def _write_paragraphs(paragraphs, stream, coding='utf8'):
    first = True
    for paragraph in paragraphs:
        if not first:
            stream.write('\n')
        first = False
        paragraph = paragraph.strip()
        paragraph = '\n'.join(textwrap.wrap(paragraph.strip()))
        if not isinstance(paragraph, unicode):
            paragraph = unicode(paragraph, 'utf8', errors='ignore')
        paragraph = paragraph.encode(coding)
        stream.write(paragraph + '\n')
