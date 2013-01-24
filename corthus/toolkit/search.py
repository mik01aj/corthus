#!/usr/bin/env python

"""
Usage: ./search.py --create-index <files>
       ./search.py --create-index `find texts/ -name '??.txt'`
            - will index all given files (should be .txt!
              note that this script uses fetcher, which can really use
              a .sentences or .huninput file)
       ./search.py <query>
            - will perform a search
"""

from __future__ import unicode_literals

import sys
import os.path

# TODO get rid of this path madness (this is relative to site-packages)
PATH_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
assert os.path.isdir(PATH_ROOT), PATH_ROOT

TEXTS_ROOT = PATH_ROOT + '/texts'
assert os.path.isdir(TEXTS_ROOT), TEXTS_ROOT

INDEX_DIR = PATH_ROOT + '/corthus/index'
assert os.path.isdir(INDEX_DIR), INDEX_DIR

EXTERNAL_DIR = PATH_ROOT + '/corthus/external' # for Whoosh
assert os.path.isdir(EXTERNAL_DIR), EXTERNAL_DIR
sys.path.append(EXTERNAL_DIR)

from Text import Text
from translit import metaphone_text
from fetcher import fetch_sentences

import whoosh.index
from whoosh.fields import *
from whoosh.qparser import QueryParser


def index_files(filenames):
    """Creates a search index from given files, and store it in the
    `INDEX_DIR` folder."""

    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
        print "Created folder " + INDEX_DIR

    schema = Schema(path=ID(stored=True, unique=True),
                    content=TEXT)

    #TODO disable stopword removal
    ix = whoosh.index.create_in(INDEX_DIR, schema)
    writer = ix.writer()

    for filename in filenames:
        try:
            print "Adding " + filename
            m = re.match('(.*)/(\w\w).txt+$', filename)
            name = m.group(1) # relative to '.'
            name_rooted = os.path.relpath(m.group(1), start=TEXTS_ROOT)
            lang = m.group(2)
            for sent_num, sent in enumerate(fetch_sentences(name, lang+'m')):
                path_str = ":".join([name_rooted, lang, str(sent_num)])
                writer.add_document(path=path_str,
                                    content=sent)
        except Exception, e:
            print "    Failed to add", filename
            print "   ", e

    writer.commit()

#def find_txt_files(directory):
#    for subdir, dirnames, filenames in os.walk(directory):
#        for filename in filenames:
#            if filename.endswith('.txt'):
#                yield os.path.join(subdir, filename)

_last_results = None

def search(query_string, page_num=1, page_length=10):
    query_string = metaphone_text(query_string)
    ix = whoosh.index.open_dir(INDEX_DIR)
    query = QueryParser("content", ix.schema).parse(query_string)
    with ix.searcher() as searcher:
        global _last_results
        _last_results = searcher.search_page(query, page_num,
                                            pagelen=page_length)
        for result in _last_results:
            [name, lang, sent_num] = result['path'].split(':')
            yield { 'name' : name,
                    'lang' : lang,
                    'sent_num' : int(sent_num) }

def get_last_results_pagecount():
    return _last_results.pagecount

def retrieve_fragment(search_result, query_string, words=50):
    r = search_result # for convenience
    sentences = fetch_sentences(TEXTS_ROOT + '/' + r['name'], r['lang'])

    n = r['sent_num']
    ws = sentences[n].split()
    for offset in range(1, 15):
        if len(ws) > words:
            break
        if n + offset < len(sentences):
            ws = ws + (sentences[n+offset].split())
        if len(ws) > words:
            break
        if n - offset >= 0:
            ws = (sentences[n-offset].split()) + ws
    return highlight(" ".join(ws), query_string)

def highlight(result, query_string):
    result_words = result.split()
    result_ms = metaphone_text(result).split()
    query_ms = metaphone_text(query_string).split()
    r = []
    last = []
    for i, word, word_m in zip(xrange(len(result_words)),
                               result_words,
                               result_ms):
        if word_m in query_ms:
            r.append(' '.join(last))
            r.append(word)
            last = []
        else:
            last.append(word)
    r.append(' '.join(last))
    assert len(r) % 2 == 1
    return r

if __name__ == '__main__':

    sys.argv = [a.decode('utf-8') for a in sys.argv]

    if not sys.argv[1:]:
        print >> sys.stderr, __doc__
        sys.exit(1)

    elif sys.argv[1] == '--create-index':
        from datetime import datetime

        print 'Creating search index in "%s"...' % INDEX_DIR
        if not sys.argv[2:]:
            print >> sys.stderr, "No files specified!"
            sys.exit(1)

        files = sys.argv[2:]

        start_time = datetime.now()
        index_files(files)
        end_time = datetime.now()
        print "Total time: %s" % (end_time - start_time)

    else:
        from textwrap import wrap

        query_string = ' '.join(sys.argv[1:])
        print "Searching for: " + query_string
        print

        for r in search(query_string):
            print r
            sentences = fetch_sentences(TEXTS_ROOT + '/' + r['name'],
                                        r['lang'])
            result_text = sentences[r['sent_num']]

            s = ""
            for i, fragment in enumerate(highlight(result_text, query_string)):
                if i%2 == 1:
                    s += " \x1b[1;31m%s\x1b[0m " % fragment
                else:
                    s += fragment
            print s
            print

