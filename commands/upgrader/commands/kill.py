from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector


CMDEXS = [
    CMDEx('kill'),
    CMDEx('kill {selector:selector}'),
]

def __upgrade(order, props):
    if len(order) == 1:
        return 'kill @s'
    else:
        return 'kill ' + selector.upgrade(props['selector'])

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)