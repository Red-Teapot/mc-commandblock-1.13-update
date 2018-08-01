from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector


CMDEXS = [
    CMDEx('xp {str:amount} {selector:player}'),
]

def __upgrade(order, props):
    result = 'xp '

    result += props['amount'] + ' '

    result += selector.upgrade(props['player']) + ' '

    if result[-1] == ' ':
        result = result[:-1]
    
    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)