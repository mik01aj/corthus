#!/usr/bin/env python

"""
Usage: python IndexFiles <directory>

It will index all .txt files found there.
"""

import sys, os, threading, time, re
import lucene
from datetime import datetime
from toolkit import Text
from toolkit.translit import metaphone_text


def index_files(filenames, storeDir):
    """Creates a search index from given files, and store it in the
    `storeDir` folder."""

    if not os.path.exists(storeDir):
        os.mkdir(storeDir)
    store = lucene.SimpleFSDirectory(lucene.File(storeDir))
    writer = lucene.IndexWriter(store, _analyzer, True,
                                lucene.IndexWriter.MaxFieldLength.LIMITED)
    writer.setMaxFieldLength(1048576)

    for filename in filenames:
        try:
            print "Adding", filename
            m = re.match('(.*)\.(\w\w).txt+$', filename)
            lang = m.group(2)
            text = Text.from_file(filename, lang=lang)
            for paragraph_num, paragraph in enumerate(text.as_paragraphs()):
                doc = lucene.Document()
                doc.add(lucene.Field("filename", filename,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.NOT_ANALYZED))
                doc.add(lucene.Field("lang", lang,
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.NOT_ANALYZED))
                doc.add(lucene.Field("num", str(paragraph_num),
                                     lucene.Field.Store.YES,
                                     lucene.Field.Index.NOT_ANALYZED))
                doc.add(lucene.Field("contents", paragraph,
                                     lucene.Field.Store.NO,
                                     lucene.Field.Index.ANALYZED))
#                doc.add(lucene.Field("metaphone", metaphone_text(paragraph),
#                                     lucene.Field.Store.NO,
#                                     lucene.Field.Index.ANALYZED))
                writer.addDocument(doc)
        except Exception, e:
            print "    Failed to add", filename
            print "   ", e

    print 'Optimizing index...',
    writer.optimize()
    writer.close()
    print 'done.'


def find_txt_files(directory):
    for subdir, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.txt'):
                yield os.path.join(subdir, filename)


lucene.initVM()
_analyzer = lucene.StandardAnalyzer(lucene.Version.LUCENE_CURRENT)


if __name__ == '__main__':
    try:
        [files_dir] = sys.argv[1:]
    except ValueError:
        print 'Using Lucene', lucene.VERSION
        print __doc__
        sys.exit(1)

    start_time = datetime.now()
    index_files(find_txt_files(files_dir), "index")
    end_time = datetime.now()
    print "Total time: %s" % (end_time - start_time)

