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
    from nltk.stem.porter import PorterStemmer
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


def __remove_stopwords(tokens):
    try:
        __stops = set(stopwords.words('english') + list(punctuation))
        return [word for word in tokens if word not in __stops]
    except Exception as e:
        logger.error(e)


def __speech_tag(tokens, nouns_verbs_only=False):
    whitelist = [
        'NNP', 'NN', 'NNS', 'NNPS',   # nouns
        'VBN', 'VBG', 'VBZ', 'VBP', 'VBD', 'VB' # verbs
    ]

    tagged = pos_tag(tokens)
    
    if nouns_verbs_only:
        return [tag for tag in tagged if tag[1] in whitelist]
    
    return [tag for tag in tagged]


def __lemmatize(tags):
    try:
        wnl = WordNetLemmatizer()
        lemmatized = []
        for tag in tags:
            # Get PoS according to WordNet req
            wnpos = lambda e: ('a' if e[0].lower() == 'j' else e[0].lower()) if e[0].lower() in ['n', 'r', 'v'] else 'n'
            lemmatized.append(wnl.lemmatize(tag[0], wnpos(tag[1])))
        return lemmatized
    except Exception as e:
        logger.error(e)
        return tags


def __stem(tags):
    try:
        porter = PorterStemmer()
        return [porter.stem(tag[0]) for tag in tags]
    except Exception as e:
        logger.error(e)
        return [tag[0] for tag in tags]


def __ner_stanford(tokens, named_only=False):
    stanford_path = os.getenv('STANFORD_NER_PATH', 'stanford_ner')
    class_path = os.path.join(stanford_path, 'classifiers/english.all.3class.distsim.crf.ser.gz')
    jar_path = os.path.join(stanford_path, 'stanford-ner.jar')
    st = StanfordNERTagger(
        class_path,
        jar_path,
        encoding='utf-8'
    )

    classified = st.tag(tokens)

    if named_only:
        return [tag for tag in classified if tag[1] != 'O']
    
    return [tag for tag in classified]


def preprocess(text, nouns_verbs_only=False, stemming=False):
    """Preprocess the input

        Performs tokenization, PoS tagging, and stemming/lemmatization

        Parameters
        ----------
        text : str
            The text to process

        nouns_verbs_only : bool
            Whether to extract verbs and nouns only. Defaults to False

        stemming : bool
            Use stemming instead of lemmatization. Defaults to False
        
        Returns
        -------
        text : str
            The processed text
    """
    # Tokenize
    tokenized = word_tokenize(text)

    # Remove stopwords
    no_stops = __remove_stopwords(tokenized)
    logger.debug(f'No stops: {no_stops}')

    # PoS tag
    tagged = __speech_tag(no_stops, nouns_verbs_only=nouns_verbs_only)
    logger.debug(f'PoS: {tagged}')

    # Stem or Lem
    if stemming:
        stemmed = __stem(tagged)
        logger.debug(f'Stemmed: {stemmed}')
        return stemmed
    else:
        # Lemmatize
        lemmatized = __lemmatize(tagged)
        logger.debug(f'Lemmatized: {lemmatized}')
        return lemmatized


def extract_stanford(text, named_only=False, stemming=False):
    """Performs entity extraction on the given text
        using Stanford's NER

        Parameters
        ----------
        text : str
            The text to process

        named_only : bool
            Get named entities only. Defaults to False

        stemming : bool
            Use stemming instead of lemmatization. Defaults to False
        
        Returns
        -------
        text : str
            The processed text
    """
    # Preprocess
    processed = preprocess(text, stemming=stemming)

    # Entity Extraction
    entities = __ner_stanford(processed, named_only=named_only)
    return ' '.join([tag[0] for tag in entities])


def extract(text, nouns_verbs_only=False, stemming=False):
    """Performs entity extraction on the given text

        Parameters
        ----------
        text : str
            The text to process

        nouns_verbs_only : bool
            Whether to extract verbs and nouns only. Defaults to False

        stemming : bool
            Use stemming instead of lemmatization. Defaults to False
        
        Returns
        -------
        text : str
            The processed text
    """
    processed = ' '.join(preprocess(text, nouns_verbs_only=nouns_verbs_only, stemming=stemming))

    # Entity Extraction
    entities = []
    for sent in sent_tokenize(processed):
        for chunk in ne_chunk(pos_tag(word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                logger.debug([f'{c[0]} : {chunk.label()}' for c in chunk])
                entities.append(' '.join([c[0] for c in chunk]))
    return ' '.join(entities)
