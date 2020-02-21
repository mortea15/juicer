import sys
from juicer.helpers.logger import rootLogger as logger

try:
    from nltk.tree import Tree
except ModuleNotFoundError as e:
    logger.error(e)
    sys.exit(2)

def prepare_result(result):
    output = []
    try:
        if isinstance(result, list):
            for item in result:
                if isinstance(item, str):
                    output.append(item)
                elif isinstance(item, tuple):
                    if isinstance(item[0], str):
                        output.append(item[0])
                    else:
                        logger.debug(f'prepare_result(): {item[0]}.type => {type(item[0])}')
                elif isinstance(item, Tree):
                    if isinstance(item[0], str):
                        output.append(item)
                    elif isinstance(item[0], tuple):
                        if isinstance(item[0][0], str):
                            output.append(item[0][0])
                        else:
                            logger.debug(f'prepare_result(): {item[0][0]}.type => {type(item[0][0])}')
                    else:
                        logger.debug(f'prepare_result(): {item[0]}.type => {type(item[0])}')
                else:
                    logger.debug(f'prepare_result(): {item}.type => {type(item)}')
        elif isinstance(result, str):
            output.append(result)
            logger.debug(f'prepare_result(): {result}.type => {type(result)}')
        else:
            logger.debug(f'prepare_result(): {result}.type => {type(result)}')
    except Exception as e:
        logger.error(e)
    
    return output