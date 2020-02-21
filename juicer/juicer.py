#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from string import punctuation

from juicer.helpers.tags import pos_tags
from juicer.helpers.logger import rootLogger as logger

try:
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.tag import StanfordNERTagger
    from nltk.corpus import stopwords
    from nltk.stem.arlstem import ARLSTem
    from nltk.stem.wordnet import WordNetLemmatizer
    from nltk import pos_tag, ne_chunk
    from nltk.data import find as find_nltk_package
except ModuleNotFoundError:
    logger.error(f'Module NLTK not found. Please install before proceeding.')
    sys.exit(2)


def check_nltk_packages(dl_path='.nltk_data', quiet=True):
    from nltk import download as nltk_download
    reqs = []
    for req in reqs:
        try:
            find_nltk_package(req, paths=[dl_path, '~/nltk_data'])
        except LookupError as e:
            logger.error(f'NLTK: Unable to find package `{req}`. ')
            logger.info(f'Downloading NLTK package `{req}`')
            try:
                nltk_download(req, download_dir=dl_path, quiet=quiet)
            except Exception as e:
                logger.error(f'NLTK: An error occurred while downloading package `{req}`.')
                logger.error(e)
                pass
    return True


def remove_stopwords(text):
    try:
        stops = set(stopwords.words('english') + list(punctuation))
        return [word for word in word_tokenize(text) if word not in stops]
    except Exception as e:
        logger.error(e)


def lemmatize(text):
    try:
        ast = ARLSTem()
        ast_stem = [ast.stem(word) for word in word_tokenize(text)]

        wnl = WordNetLemmatizer()
        wnl_stem = [wnl.lemmatize(word) for word in word_tokenize(text)]

        return wnl_stem
    except Exception as e:
        logger.error(e)


def speech_tag(text, whitelisted=False):
    whitelist = [
        'NNP', 'NN', 'NNS', 'NNPS',   # nouns
        'VBN', 'VBG', 'VBZ', 'VBP', 'VBD', 'VB' # verbs
    ]

    tagged = pos_tag(word_tokenize(text))
    
    if whitelisted:
        return [tag for tag in tagged if tag[1] in whitelist]
    
    return tagged


def extract_entities(text, whitelisted=False):
    entities = []
    for sentence in sent_tokenize(text):
        chunks = ne_chunk(speech_tag(sentence, whitelisted=whitelisted))
        entities.extend([chunk for chunk in chunks if hasattr(chunk, 'label')])
    return entities


def ner_stanford(text, named_only=True):
    stanford_path = os.getenv('STANFORD_NER_PATH', 'stanford_ner')
    class_path = os.path.join(stanford_path, 'classifiers/english.all.3class.distsim.crf.ser.gz')
    jar_path = os.path.join(stanford_path, 'stanford-ner.jar')
    st = StanfordNERTagger(
        class_path,
        jar_path,
        encoding='utf-8'
    )

    tokenized = word_tokenize(text)
    classified = st.tag(tokenized)

    if named_only:
        return [tag for tag in classified if tag[1] is not 'O']
    
    return classified


def process_text(text, named_only=True):
    """Removes stopwords, lemmatizes each word and returns the processed text
    """
    logger.debug(f'Pre: {text}')
    nostops = remove_stopwords(text)
    logger.debug(f'No stops: {nostops}')
    lemmatized = lemmatize(' '.join(nostops))
    logger.debug(f'Lemmatized: {lemmatized}')
    named_ents = ner_stanford(' '.join(lemmatized), named_only=named_only)
    logger.debug(f'NER: {named_ents}')
    return named_ents