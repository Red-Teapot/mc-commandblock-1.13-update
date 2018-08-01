from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector


CMDEXS = [
    CMDEx('tell {selector:player} {*:message}'),
]

def __upgrade(order, props):
    result = 'tell ' + selector.upgrade(props['player']) + ' '

    result += props['message']

    if result[-1] == ' ':
        result = result[:-1]

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)