#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import os
import sys

import juicer
from juicer.helpers.logger import rootLogger as logger
from juicer.helpers.logger import increase_log_level, log_to_file
from juicer.helpers.utils import prepare_result

current = os.path.realpath(os.path.dirname(__file__))
APPNAME = 'juicer'


INDENT = '  '
HELPMSG = f'''usage: {APPNAME} (-f <FILE_PATH> | -s) [-a] [--ner] [--nvo] [-p] [-e] [-x] [-c] [-v] [-g]

    Input:
    {INDENT * 1}-f, --infile        {INDENT * 2}Extract entities from file
    {INDENT * 1}-s, --stdin         {INDENT * 2}Extract entities from STDIN

    Options:
    {INDENT * 1}-a, --all           {INDENT * 2}Extract all entities for `--process`. (default: named entities only)
    {INDENT * 1}--ner               {INDENT * 2}Enable Named Entity Recognition for `--process`. (default: disabled)
    {INDENT * 1}--nvo               {INDENT * 2}Extract verbs and nouns only
    {INDENT * 1}--stem              {INDENT * 2}Use stemming (PorterStemmer) instead of lemmatization

    Actions:
    {INDENT * 1}-p, --process       {INDENT * 2}Preprocess the input (stopword removal, lemmatization/stemming)

    {INDENT * 1}-e, --extract       {INDENT * 2}Extract entities from the text
    {INDENT * 1}-x, --stanford      {INDENT * 2}Extract entities from the text using Stanford NER. (Use with -a to extract all entities).


    {INDENT * 1}-c, --check         {INDENT * 2}Check if all required NLTK packages are present. Downloads missing packages.

    {INDENT * 1}-v, --verbose       {INDENT * 2}Increase verbosity (can be used several times, e.g. -vvv)
    {INDENT * 1}-g, --log-file      {INDENT * 2}Write log events to the file `{APPNAME}.log`
    {INDENT * 1}--help              {INDENT * 2}Print this message
'''


def main():
    TEXT = None
    CONFIG = {
        'ner': False,
        'outfile': None,
        'format': 'plain',
        'nvo': False,
        'stem': False
    }

    result = None

    if len(sys.argv) < 2:
        print(HELPMSG)
        logger.error('No file specified')
        sys.exit(2)
    
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, 'f:sapexcvg', ['infile=', 'stdin', 'all', 'ner', 'nvo', 'stem', 'process', 'extract', 'stanford', 'check', 'verbose', 'log-file', 'help'])
    except getopt.GetoptError as e:
        print(HELPMSG)
        print(e)
        sys.exit(2)

    if not opts:
        print(HELPMSG)
        sys.exit(0)

    """
    Increase verbosity
    """
    opts_v = len(list(filter(lambda opt: opt == ('-v', ''), opts)))
    if opts_v > 4:
        opts_v = 4
    v = 0
    while v < opts_v:
        increase_log_level()
        v += 1
    
    """
    Log to file
    """
    if v > 0:
        enable_logfile = list(filter(lambda opt: opt[0] in ('-l', '--log-file'), opts))
        if enable_logfile:
            log_to_file()
    
    for opt, arg in opts:
        if opt == '--help':
            print(HELPMSG)
            sys.exit(0)
        elif opt in ('-c', '--check'):
            juicer.check_nltk_packages()

        elif opt in ('-f', '--infile'):
            file_path = arg
            logger.debug(f'Using input file {file_path}')
            try:
                with open(file_path, 'r') as f:
                    TEXT = f.read()
            except Exception as e:
                logger.error(f'An error occurred while reading the file `{file_path}`.')
                logger.error(e)
                sys.exit(2)
        elif opt in ('-s', '--stdin'):
            try:
                logger.debug(f'Using input from STDIN')
                TEXT = sys.stdin.read()
            except Exception as e:
                logger.error(e)
                sys.exit(2)
        elif opt == '--ner':
            logger.debug(f'CONFIG: Named Entity Extraction enabled')
            CONFIG['ner'] = True
        elif opt in ('--nvo'):
            logger.debug(f'CONFIG: Verbs and Nouns only')
            CONFIG['nvo'] = True
        elif opt in ('--stem'):
            logger.debug('CONFIG: Stemming enabled')
            CONFIG['stem'] = True
        elif opt in ('-e', '--extract'):
            if TEXT:
                logger.debug(f'ACTION: Extracting entities')
                result = juicer.extract(TEXT, nouns_verbs_only=CONFIG.get('nvo', False), stemming=CONFIG.get('stem', False))
            else:
                logger.error(f'Missing input (specify using -f or -s)')
                sys.exit(2)
        elif opt in ('-x', '--stanford'):
            if TEXT:
                logger.debug(f'ACTION: Stanford Named Entity Recognition')
                result = juicer.extract_stanford(TEXT, named_only=CONFIG.get('ner', False), stemming=CONFIG.get('stem', False))
            else:
                logger.error(f'Missing input (specify using -f or -s)')
                sys.exit(2)
        elif opt in ('-p', '--process'):
            if TEXT:
                logger.debug(f'ACTION: Preprocessing text')
                result = juicer.preprocess(TEXT, nouns_verbs_only=CONFIG.get('nvo', False), stemming=CONFIG.get('stem', False))
            else:
                logger.error(f'Missing input (specify using -f or -s)')
                sys.exit(2)
        
    if result:
        if isinstance(result, str):
            print(result)
        elif isinstance(result, list):
            print(' '.join(result))
        else:
            print(result)
        sys.exit(0)


if __name__ == '__main__':
    main()
