from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import entity


CMDEXS = [
    CMDEx('summon {id:id}'),
    CMDEx('summon {id:id} {coordinate:x} {coordinate:y} {coordinate:z}'),
    CMDEx('summon {id:id} {coordinate:x} {coordinate:y} {coordinate:z} {nbtstr:nbt}'),
]

def __upgrade(order, props):
    id = entity.upgrade(props['id'])

    result = 'summon '

    result += id + ' '

    if 'x' in props:
        result += str(props['x']) + ' '

    if 'y' in props:
        result += str(props['y']) + ' '

    if 'z' in props:
        result += str(props['z']) + ' '
    
    if 'nbt' in props:
        result += str(props['nbt']) + ' '
    
    if result[-1] == ' ':
        result = result[:-1]

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)