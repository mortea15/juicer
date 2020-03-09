#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import os
import sys

import juicer
from juicer.helpers.logger import rootLogger as logger
from juicer.helpers.logger import increase_log_level
from juicer.helpers.utils import prepare_result

current = os.path.realpath(os.path.dirname(__file__))
APPNAME = 'juicer'


INDENT = '  '
HELPMSG = f'''usage: {APPNAME} (-f INPUT_FILE | -s) [-a] [-w] [-p] [-r] [-l] [-t] [-e] [-n] [-d FORMAT] [-o OUTPUT_FILE] [-c] [-v]

    {INDENT * 1}-f, --infile        {INDENT * 2}Extract entities from file
    {INDENT * 1}-s, --stdin         {INDENT * 2}Extract entities from STDIN

    {INDENT * 1}-a, --all           {INDENT * 2}Extract all entities (default is named entities only)
    {INDENT * 1}-w, --whitelist     {INDENT * 2}Extract whitelisted tags only (verbs and nouns)

    {INDENT * 1}-p, --process       {INDENT * 2}Process the input and output entities
    {INDENT * 1}-r, --remove-stops  {INDENT * 2}Remove stopwords
    {INDENT * 1}-l, --lemmatize     {INDENT * 2}Lemmatize the text (stemming)
    {INDENT * 1}-t, --speech-tag    {INDENT * 2}POS tag the text
    {INDENT * 1}-e, --extract       {INDENT * 2}Extract entities from the text
    {INDENT * 1}-n, --stanford      {INDENT * 2}Entity extraction using the Stanford NER. (Use with -a to extract all entities).

    {INDENT * 1}-o, --outfile       {INDENT * 2}Output results to this file
    {INDENT * 1}-d, --format        {INDENT * 2}Output results as this format.
                              Available formats: [plain (default), json]

    {INDENT * 1}-c, --check         {INDENT * 2}Check if all required NLTK packages are present. Downloads missing packages.

    {INDENT * 1}-v, --verbose       {INDENT * 2}Increase verbosity (can be used twice, e.g. -vv)
    {INDENT * 1}--help              {INDENT * 2}Print this message
'''


def main():
    TEXT = None
    CONFIG = {
        'named': True,
        'outfile': None,
        'format': 'plain',
        'whitelisted': False
    }

    result = None

    if len(sys.argv) < 2:
        print(HELPMSG)
        logger.error('No file specified')
        sys.exit(2)
    
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, 'f:sawprlteno:d:cv', ['infile=', 'stdin', 'all', 'process', 'remove-stops', 'lemmatize', 'speech-tag', 'whitelist', 'extract', 'stanford', 'outfile=', 'format=', 'check', 'verbose', 'help'])
    except getopt.GetoptError:
        print(HELPMSG)
        sys.exit(2)

    if not opts:
        print(HELPMSG)
        sys.exit(0)

    """
    Increase verbosity
    """
    opts_v = len(list(filter(lambda opt: opt == ('-v', ''), opts)))
    if opts_v > 2:
        opts_v = 2
    v = 0
    while v < opts_v:
        increase_log_level()
        v += 1
    
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
        elif opt in ('-a', '--all'):
            logger.debug(f'CONFIG: Extracting all entities')
            CONFIG['named'] = False
        elif opt in ('-w', '--whitelist'):
            logger.debug(f'CONFIG: Enabling whitelist')
            CONFIG['whitelisted'] = True
        elif opt in ('-r', '--remove-stops'):
            if TEXT:
                logger.debug(f'ACTION: Removing stopwords')
                result = juicer.remove_stopwords(TEXT)
            else:
                logger.error(f'Missing input (specify using -f or -s)')
                sys.exit(2)
        elif opt in ('-l', '--lemmatize'):
            if TEXT:
                logger.debug(f'ACTION: Lemmatizing')
                result = juicer.lemmatize(TEXT)
            else:
                logger.error(f'Missing input (specify using -f or -s)')
                sys.exit(2)
        elif opt in ('-t', '--speech-tag'):
            if TEXT:
                logger.debug(f'ACTION: Speech tagging')
                result = juicer.speech_tag(TEXT, whitelisted=CONFIG.get('whitelisted', False))
            else:
                logger.error(f'Missing input (specify using -f or -s)')
                sys.exit(2)
        elif opt in ('-e', '--extract'):
            if TEXT:
                logger.debug(f'ACTION: Extracting entities')
                result = juicer.extract_entities(TEXT, whitelisted=CONFIG.get('whitelisted', False))
            else:
                logger.error(f'Missing input (specify using -f or -s)')
                sys.exit(2)
        elif opt in ('-n', '--stanford'):
            if TEXT:
                logger.debug(f'ACTION: Stanford Named Entity Recongition')
                result = juicer.ner_stanford(TEXT, named_only=CONFIG.get('named', False))
            else:
                logger.error(f'Missing input (specify using -f or -s)')
                sys.exit(2)
        elif opt in ('-p', '--process'):
            if TEXT:
                logger.debug(f'ACTION: Processing text')
                result = juicer.process_text(TEXT, named_only=CONFIG.get('named', True))
            else:
                logger.error(f'Missing input (specify using -f or -s)')
                sys.exit(2)

        elif opt in ('-o', '--outfile'):
            logger.debug(f'CONFIG: Setting output file to {arg}')
            CONFIG['outfile'] = arg
        elif opt in ('-d', '--format'):
            if arg in ['plain', 'json']:
                logger.debug(f'CONFIG: Setting output file format to {arg}')
                CONFIG['format'] = arg
            else:
                logger.error('Invalid format. Must be one of [plain, json]')
                sys.exit(2)
        
    if result:
        output = prepare_result(result)

        outfile = CONFIG.get('outfile')
        outformat = CONFIG.get('format')
        if outfile:
            ext = 'json' if outformat == 'json' else 'txt'
            fname = f'{outfile}.{ext}'
            if outformat == 'plain':
                with open(fname, 'w') as f:
                    f.write('\n'.join(output))
            elif outformat == 'json':
                import json
                with open(fname, 'w', encoding='utf-8') as f:
                    json.dump(output, f, ensure_ascii=False, indent=4)
            logger.info(f'Results saved to file `{fname}`')
            sys.exit(0)
        else:
            print('\n'.join(output))
            sys.exit(0)


if __name__ == '__main__':
    main()
