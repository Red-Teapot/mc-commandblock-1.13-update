import pkgutil, logging

from ..pre_1_13.cmdex import CMDEx
from . import commands


logger = logging.getLogger(__name__)

CMD_UPGRADERS = dict()

for loader, module_name, is_pkg in pkgutil.walk_packages(commands.__path__):
    full_name = commands.__name__ + '.' + module_name
    module = loader.find_module(full_name).load_module(full_name)
    
    if hasattr(module, 'upgrade'):
        CMD_UPGRADERS[module_name] = module.upgrade
    else:
        logger.warning('No upgrade method in module %s, skipping', module.__name__)

def upgrade(command: str) -> str:
    command = command.strip()

    if command[0] == '/':
        command = command[1:]
    
    if command.find(' ') >= 0:
        name = command[:command.find(' ')]
    else:
        name = command

    if name in CMD_UPGRADERS:
        return CMD_UPGRADERS[name](command)
    else:
        raise Warning('Unknown command: \'{}\', leaving as is'.format(command))