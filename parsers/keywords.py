#!/usr/bin/env python3

"""
This script extracts keywords from .txt files,
that consist of terms divided by paragraphs.
"""


import os
import sys
import re
import json
import logging
import argparse

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from utils.text import TextProcessor, remove_urls


LOG = logging.getLogger(__name__)


def lang_files_iterator(lang, dirname):
    patt = re.compile(r'%s(\-{1}\w+){0,1}.txt$' % lang)
    for root, dirs, files in os.walk(dirname):
        for fname in files:
            if patt.match(fname):
                yield lang, os.path.join(root, fname)


def all_files_iterator(dirname):
    for root, dirs, files in os.walk(dirname):
        for fname in files:
            lang = fname[:2]
            path = os.path.join(root, fname)
            if os.path.isfile(path) and fname.endswith('.txt'):
                yield lang, path


def file_iter(**kwargs):
    language = kwargs.get('lang', None)
    dirname = kwargs['source_dir'][0]
    if language:
        return lang_files_iterator(language, dirname)

    return all_files_iterator(dirname)


def extract_terms(fname, **kwargs):
    with open(fname, 'r') as fp:
        lines = [x.strip() for x in fp.readlines()]
        fp.close()

        return remove_urls(lines)


def extract_keywords(lang, terms):
    tokens = []
    proc = TextProcessor(lang)
    text = "\n".join(terms)
    tokens = proc.clean(text)

    # Warning: a possible alternative to proc.vectors:
    # https://towardsdatascience.com/summarizing-the-great-gatsby-using-natural-language-processing-9248ab8e9483
    #
    # from utils.vectors import build_adjacency_matrix, \
    #      calc_stationary_probabilities, output_summary
    # term_map = [(term.value, cleaner.clean(term)) for term in terms]
    # adjacency_matrix = build_adjacency_matrix(term_map)
    # prob_distribution = calc_stationary_probabilities(adjacency_matrix)
    # output_summary(prob_distribution[0], term_map, 10)
    #
    return proc.vectors(tokens, top_N=100)


def main(**kwargs):
    data = {}
    for lang, fname in file_iter(**kwargs):
        terms = extract_terms(fname, **kwargs)
        try:
            data[lang]['terms'].extend(terms)
        except KeyError:
            data[lang] = {'terms': terms}

    for lang, val in data.items():
        data[lang]['keywords'] = extract_keywords(lang, val['terms'])
        print(json.dumps(data[lang]['keywords'], indent=4))


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
        nargs='?',
        dest='lang',
        default=None,
        help='2 symbols language code (e.g. `en`). Default: %(default)s (process all languages)'
    )
    parser.add_argument(
        'source_dir',
        nargs=1,
        type=str,
        help='Directory with source files <lang>.txt.'
    )
    args = parser.parse_args()
    kwargs = vars(args)
    main(**kwargs)
