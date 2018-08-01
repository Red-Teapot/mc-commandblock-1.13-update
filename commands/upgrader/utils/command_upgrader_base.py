import logging
from commands.pre_1_13.cmdex import CMDEx


logger = logging.getLogger(__name__)

def upgrade(CMDEXs: list, command: str, callback: callable) -> str:
    order = None
    props = None

    logger.debug('Matching command \'%s\'', command)

    found = False

    for cmdex in CMDEXs:
        try:
            logger.debug('Matching CMDEx \'%s\'', str(cmdex))
            order, props = cmdex.match(command)
            logger.debug('Match')
            found = True
            break
        except:
            pass
    
    if not found:
        raise Exception('Unknown syntax for command \'{}\''.format(command))
    
    return callback(order, props)