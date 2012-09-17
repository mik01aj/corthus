# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import os.path
import re
from datetime import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, redirect
from django.template import Template, RequestContext, loader

from www.settings import TEXTS_ROOT

from toolkit.fetcher import fetch_sentences, fetch_alignment
from toolkit.translit import render_cu
import toolkit.search as ts

def index(request):
    return redirect('/texts/')
#    template = loader.get_template('base.html')
#    context = RequestContext(request, { 'title': 'index' })
#    return HttpResponse(template.render(context))

def text(request, basename, langs):

    # determining languages
    if langs == 'default':
        if 'langs' in request.COOKIES:
            langs = request.COOKIES['langs']
        else:
            langs = "pl-cu"
        return redirect('/texts/' + basename + '.' + langs)
    langs = langs.split('-')

    def as_table(alignment, seqs, langs):
        """Converts an aligmnent to a HTML table.
        """
        n = len(seqs)
        sents_waiting = [[] for i in xrange(n)]
        table_row = None
        all_ranges = alignment.as_ranges(with_costs=False)
        for rung_num, rung_ranges in enumerate(all_ranges):
            assert len(rung_ranges) == len(seqs)

            # finishing the cell (if ¶ everywhere or similar situation)
            all_break = all(s >= len(seq) or s==e
                            or seq[s] == '¶' or seq[s-1] == '¶'
                            for (seq, (s, e)) in zip(seqs, rung_ranges))
            if (all_break or rung_num == len(all_ranges)-1) and table_row:
                if any(cell['sentences'] for cell in table_row):
                    yield table_row
                table_row = None

            # starting new table_row
            if not table_row:
                table_row = []
                for (lang, (s, e)) in zip(langs, rung_ranges):
                    table_row.append({ 'sentences' : [],
                                       'lang' : lang,
                                       'rung' : rung_num,
                                       'rowspan' : 1, })
                assert len(table_row) == n

            # adding sentences to each column
            for (column, seq, lang, (s, e)) in \
                    zip(xrange(n), seqs, langs, rung_ranges):
                if s < len(seq) and seq[s] == '¶' and not table_row[column]['sentences']:
                    s += 1 # don't start a cell with an empty paragraph
                for sent, sent_num in zip(seq[s:e], range(s, e)):
                    table_row[column]['sentences'].append(
                        { 'text': _render_sentence(sent, lang),
                          'is_break' : sent == '¶',
                          'rung_num' : rung_num,
                          'num' : sent_num })

        yield table_row

    # getting navigation links
    other_basenames = set()
    navigation_links = []
    for f in os.listdir(os.path.dirname(TEXTS_ROOT + '/' + basename)):
        if f.endswith('.txt'):
            other_basenames.add(f.split('.')[0])
    other_basenames = sorted(other_basenames)
    for f in other_basenames:
        navigation_links.append({ 'href' : f + '.' + '-'.join(langs),
                                  'label' : f,
                                  'current' : os.path.basename(basename) == f})
    link_up = { 'href': '.',
                'label': os.path.basename(os.path.dirname(basename)) }

    # checking language availability
    available_langs = [lang
                       for lang in ['pl', 'cu', 'el']
                       if os.path.exists("%s/%s/%s.txt" %
                                         (TEXTS_ROOT, basename, lang))]
    #print available_langs
    all_langs_available = False
    for lang in langs:
        if lang[:2] not in available_langs:
            error_message = "Language %s is not available for this text." % lang
            template = loader.get_template('error.html')
            context = RequestContext(request,
                                     { 'error_message' : error_message,
                                       'navigation_links' : navigation_links,
                                       'request' : request })
            return HttpResponse(template.render(context))

    # getting alignment
    a = None
    for backend in ('golden', 'my', 'hunalign'):
        try:
            a = fetch_alignment(TEXTS_ROOT + '/' + basename, langs, backend)
            break # note: variable 'backend' remains set
        except IOError:
            pass
    if not a:
        raise Http404

    # getting texts
    try:
        ts = [fetch_sentences(TEXTS_ROOT + '/' + basename, lang)
              for lang in langs]
    except IOError:
        raise Http404

    # creating table
    table = list(as_table(a, ts, langs))

    info = 'Using backend: ' + backend

    # getting corrections
    try:
        with open(TEXTS_ROOT + '/' + basename + '/' + '-'.join(langs) + '.hand') as f:
            corrections = f.read()
    except IOError:
        corrections = ''

    template = loader.get_template('text.html')
    context = RequestContext(request,
                             { 'title' : os.path.basename(basename),
                               'up' : link_up,
                               'info' : info,
                               'langs' : '-'.join(langs),
                               'table' : table,
                               'col_width' : 100/len(langs),
                               'navigation_links' : navigation_links,
                               'corrections' : corrections,
                               'request' : request })
    return HttpResponse(template.render(context))


def correct(request, basename, langs):
    data = request.POST['corrections']
    for line in data.splitlines():
        if not re.match('\d+\t\d+\t?$', line):
            print line
            return HttpResponse('invalid data :(', status=500)
    # TODO some more data checking
    with open(TEXTS_ROOT + '/' + basename + '/' + langs + '.hand', 'w') as f:
        f.write(data)
    return redirect('/texts/' + basename + '.' + langs)

def search(request):
    query = request.GET['q']
    if 'p' in request.GET:
        page_num = int(request.GET['p'])
    else:
        page_num = 1
    page_length = 15

    results = []

    start_time = datetime.now()
    for r in ts.search(query, page_num, page_length=page_length):
        sentences = fetch_sentences(TEXTS_ROOT + '/' + r['name'], r['lang'])
        r['fragments'] = [_render_sentence(f, r['lang'])
                          for f in ts.retrieve_fragment(r, query)]
        r['link'] = ('/texts/%s.%s#%s-%s' %
                     (r['name'], r['lang'], r['lang'], r['sent_num']))
        results.append(r)
    timedelta = datetime.now() - start_time
    time_elapsed = timedelta.seconds + timedelta.microseconds/1000000.0
    page_count = ts.get_last_results_pagecount()
    stats = "Showing page %d of %d (time: %.2fs)" % (page_num, page_count,
                                                     time_elapsed)

    template = loader.get_template('search.html')
    context = RequestContext(request,
                             { 'title': 'Searching for: ' + query,
                               'info' : stats,
                               'query' : query,
                               'page_num' : page_num,
                               'page_count' : page_count,
                               'results' : results,
                               'request' : request })
    return HttpResponse(template.render(context))

def folder(request, requested_path):

    if not requested_path.endswith('/'):
        return redirect('/texts' + requested_path + '/')

    if requested_path == '/':
        title = 'Index of Books'
        link_up = None
    else:
        title = requested_path[1:-1] + ' - Table of Contents'
        link_up = { 'href' : '/texts' + os.path.dirname(requested_path[:-1]) }
    requested_path = TEXTS_ROOT + '/' + requested_path

    try:
        fs = sorted(os.listdir(requested_path))
    except OSError:
        raise Http404

    dirs = []
    by_names = {}
    for f in fs:
        if not os.path.isdir(os.path.join(requested_path, f)):
            continue
        ls = []
        for lang in ['pl', 'cu', 'el']:
            if os.path.exists(os.path.join(requested_path, f, lang + ".txt")):
                ls.append(lang)
        if ls:
            by_names[f] = ls
        else:
            dirs.append(f)

    template = loader.get_template('folder.html')
    context = RequestContext(request,
                             { 'title' : title,
                               'dirs' : dirs,
                               'up' : link_up,
                               'by_names' : sorted(by_names.items()),
                               'request' : request })
    return HttpResponse(template.render(context))





def _render_sentence(sent, lang):
    if lang in ('cu', 'cue'):
        return render_cu(sent)
    return sent

