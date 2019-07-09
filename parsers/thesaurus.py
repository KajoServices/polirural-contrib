#!/usr/bin/env python3

"""
This script extracts terms from thesaurus (RDF)
and saves them as text files (one file per language).
"""


import os
import sys
import six
import logging
import argparse

import rdflib

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from conf import settings
from utils.text import TextCleaner, remove_urls
from utils.generic import RecordDict


logging.root.setLevel(logging.NOTSET)
LOG = logging.getLogger('console')


def err_format(error):
    return "(%s) %s" % (type(error), str(error))


def log(method, msg, *args, **kwargs):
    if kwargs.get('verbose', True):
        meth = getattr(LOG, method)
        meth(msg, *args)


def register_token(value, language, **kwargs):
    log('info', "%s: %s", language, value, **kwargs)
    save_to = kwargs.get('save_to', None)
    if not save_to:
        return

    dest_dirname = os.path.join(save_to, "langs")
    if not os.path.exists(dest_dirname):
        log('warning', '..creating directory: %s', dest_dirname, **kwargs)
        os.makedirs(dest_dirname)

    fname = os.path.join(dest_dirname, "{}.txt".format(language))
    if not os.path.exists(fname):
        log('warning', '...creating %s', fname, **kwargs)

    with open(fname, "a+") as fp:
        fp.write(value+"\n")
        fp.close()


def rdf_parse(fname):
    graph = rdflib.Graph()
    return graph.parse(fname)


def parse_graph(fname, **kwargs):
    lang = kwargs.get('lang', None)
    lang_unknown = 'xx'
    graph = rdf_parse(fname)
    for node in graph:
        for chunk in node:
            if not (isinstance(chunk, rdflib.term.Literal) and
                    isinstance(chunk.value, six.string_types)):
                continue

            language = lang_unknown
            # TODO: if lang is None, use Polyglot to detect it.
            try:
                if chunk.language:
                    language = chunk.language
            except Exception as err:
                log('error', err_format(err), **kwargs)
                continue

            # Skip the Literal, in which language isn't specified,
            # or not the one provided in params (check the latter
            # using `startswith` for not all languages are defined by
            #  2 symbols (examples: 'en_us', 'es-419', 'pt-br')
            if lang and (not language.startswith(lang)):
                continue

            register_token(chunk.value, language, **kwargs)

    log('info', "Done", **kwargs)
    save_to = kwargs.get('save_to', None)
    if save_to:
        log('info', "see %s", save_to, **kwargs)


def main(**kwargs):
    for src in kwargs['sources']:
        parse_graph(src, **kwargs)

    log('info', 'Done', **kwargs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='verbose',
        default=True,
        help='Be talkative [default: %(default)s]'
    )
    parser.add_argument(
        '-l', '--lang',
        type=str,
        dest='lang',
        default=None,
        help='2 symbols language code (e.g. `en`). Default: %(default)s (process all languages)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        dest='save_to',
        default=None,
        help='Directory to save keywords to. If not given, results printed to stdout.'
    )
    parser.add_argument(
        'sources',
        nargs='+',
        type=str,
        help='RDF filename (one or more).'
    )
    args = parser.parse_args()
    kwargs = vars(args)
    main(**kwargs)
