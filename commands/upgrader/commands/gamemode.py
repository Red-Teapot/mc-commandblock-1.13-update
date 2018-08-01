from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector
from .. import data


CMDEXS = [
    CMDEx('gamemode {str:mode}'),
    CMDEx('gamemode {str:mode} {selector:player}'),
]

def __upgrade(order, props):
    result = 'gamemode '

    result += data.gamemode_map[props['mode']] + ' '

    if 'player' in props:
        result += selector.upgrade(props['player']) + ' '
    
    if result[-1] == ' ':
        result = result[:-1]
    
    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)