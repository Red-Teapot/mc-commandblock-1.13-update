from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector


CMDEXS = [
    CMDEx('stopsound {selector:player}'),
    CMDEx('stopsound {selector:player} {str:source}'),
    CMDEx('stopsound {selector:player} {str:source} {str:sound}'),
]

def __upgrade(order, props):
    result = 'stopsound ' + selector.upgrade(props['player']) + ' '
    if 'source' in props:
        result += props['source'] + ' '
    if 'sound' in props:
        result += props['sound'] + ' '
    if result[-1] == ' ':
        result = result[:-1]
    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)