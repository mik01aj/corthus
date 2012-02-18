# -*- coding: utf-8 -*-

import codecs

class Text(object):
    """A class that makes text available in various formats.  It is
    pretty lightweight, so it can be used just to read paragraphs of
    test from a file. All text data is stored internally as unicode
    strings.
    """

    def __init__(self, data, lang=None, coding='utf-8', name=None):
        """Create a string from given data.
        data: a string or stream (e.g. an open file)
        """
        assert lang==None or (isinstance(lang, (unicode, str)) and len(lang)==2)
        if isinstance(data, (str, unicode)):
            data = StringIO(data)
        self.paragraphs = tuple(_read_paragraphs(data, coding))
        self.lang = lang
        self.name = name

    @classmethod
    def from_file(cls, path, *args, **kwargs):
        with codecs.open(path, encoding=kwargs.get('coding', 'utf-8')) as f:
            return Text(f, *args, **kwargs)

    def as_string(self):
        stream = StringIO()
        _write_paragraphs(self.paragraphs, stream)
        return stream.getvalue()

    def as_paragraphs(self):
        return self.paragraphs

    def as_sentences(self, paragraph_separator=None):
        def gen():
            for p in self.paragraphs:
                for sent in nlp.sent_tokenize(self.lang, p):
                    yield sent
                if paragraph_separator:
                    yield paragraph_separator
        return list(gen())

    def as_sentences_flat(self):
        return self.as_sentences(paragraph_separator=u'¶')

    def as_sentences_nested(self):
        return [ list(nlp.sent_tokenize(self.lang, p))
                 for p in self.paragraphs ]

    # maybe also as words?

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
