from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector


CMDEXS = [
    CMDEx('spawnpoint {selector:player}'),
    CMDEx('spawnpoint {selector:player} {coordinate:x} {coordinate:y} {coordinate:z}'),
]

def __upgrade(order, props):
    result = 'spawnpoint '
    result += selector.upgrade(props['player']) + ' '

    if 'x' in props:
        result += str(props['x']) + ' '
        result += str(props['y']) + ' '
        result += str(props['z']) + ' '
    
    if result[-1] == ' ':
        result = result[:-1]
    
    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)