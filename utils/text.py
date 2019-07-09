import string

import spacy
import validators
from collections import OrderedDict


PUNC_TAB = str.maketrans('', '', string.punctuation)
models = {'en': 'en_core_web_md'}


def ls(text):
    return text.lower().strip()


def remove_urls(terms):
    """Remove URLs from the <list> of terms."""
    return [t.strip() for t in terms if not validators.url(t)]


class TextProcessor:
    punctable = str.maketrans('', '', string.punctuation)
    digits = str.maketrans('', '', string.digits)

    def __init__(self, lang, *args, **kwargs):
        """
        :param text: <str>
        :param lang: <str>
        """
        # TODO: make it downloadable, if absent (use tenacity)
        self.nlp = spacy.load(models[lang])

        # Warning! `max_length = 2_500_000` is safe, ONLY if not using NER!
        #          Otherwise change to default (1_000_000)
        self.nlp.max_length = 2500000
        self.tokenizer = spacy.tokenizer.Tokenizer(self.nlp.vocab)

    @staticmethod
    def remove_punct(tock):
        return tock.translate(TextProcessor.punctable)

    @staticmethod
    def remove_digits(tock):
        return tock.translate(TextProcessor.digits)

    def clean(self, text):
        txt = self.remove_punct(text)
        txt = self.remove_digits(txt)

        tokens = self.tokenizer(txt)
        tokens = [token.lemma_.lower() for token in tokens
                  if not token.is_punct | token.is_space | token.is_stop]

        return tokens

    def vectors(self, tokens, top_N=None):
        vects = []
        for token in self.nlp(" ".join(tokens)):
            vects.append({
                'text': token.text,
                'norm': token.vector_norm
                })
        vects = sorted(vects, key=lambda x: x['norm'], reverse=True)

        cnt = 0
        result = OrderedDict()
        keys = []
        for vect in vects:
            if cnt == top_N:
                break

            if vect['text'] in keys:
                continue

            result[vect['text']] = float(vect['norm'])
            keys.append(vect['text'])
            cnt += 1

        return result
