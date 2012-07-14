#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.

Usage: ./search.py <query>

Documentation of Lucene's query syntax:
http://lucene.apache.org/core/3_6_0/queryparsersyntax.html
"""

import lucene
import atexit
import sys
from file_info import get_info
from toolkit import Text

#def get_result_info(scoreDoc):
#    doc = _searcher.doc(scoreDoc.doc)
#    filename = doc.get("path")
#    info = get_info(path)
#    text = Text.from_file(filename, lang=info['lang'])
#    return


lucene.initVM()

_index_directory = lucene.SimpleFSDirectory(lucene.File("index"))

_searcher = lucene.IndexSearcher(_index_directory, True)
atexit.register(lambda: _searcher.close()) # _searcher closed automatically at exit

_analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)

_parser = lucene.QueryParser(lucene.Version.LUCENE_CURRENT, "contents", _analyzer)
_parser.setAllowLeadingWildcard(True);


if __name__ == '__main__':
    from textwrap import wrap

    query_string = unicode(' '.join(sys.argv[1:]), 'utf-8')
    if not query_string:
        print 'Using Lucene', lucene.VERSION
        print __doc__
        sys.exit(1)

    texts = {}

    print "Searching for:", query_string
    query = _parser.parse(query_string)

    for scoreDoc in  _searcher.search(query, 50).scoreDocs:
        #print scoreDoc
        doc = _searcher.doc(scoreDoc.doc)
        filename = doc.get("filename")
        try:
            text = texts[filename]
        except KeyError:
            text = Text.from_file(filename,
                                  lang=doc.get("lang"))
            text = list(text.as_paragraphs())
            texts[filename] = text
        print "%s : %s" % (filename, doc.get("num"))
        paragraph_index = int(doc.get("num"))
        found_paraghaph = text[paragraph_index]

        stream = lucene.TokenSources.getTokenStream("contents", found_paraghaph, _analyzer);
        scorer = lucene.Scorer(query, "contents", lucene.CachingTokenFilter(stream))
        highligter = lucene.Highligter(scorer)
        fragment = highligter.getBestFragment(_analyzer, "contents",
                                              found_paraghaph)
        print '>>>' + fragment

        for line in wrap(found_paraghaph):
            print '   ', line



