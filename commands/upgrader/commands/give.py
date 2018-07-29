from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import selector, command_upgrader_base, item


CMDEXS = [
    CMDEx('give {selector:player} {id:id}'),
    CMDEx('give {selector:player} {id:id} {int:count}'),
    CMDEx('give {selector:player} {id:id} {int:count} {int:metadata}'),
    CMDEx('give {selector:player} {id:id} {int:count} {int:metadata} {nbtstr:nbt}'),
]

def __upgrade(order, props):
    player = selector.upgrade(props['player'])

    id = props['id']

    if 'metadata' in props:
        metadata = props['metadata']
    else:
        metadata = None
    
    if 'nbt' in props:
        nbt = props['nbt']
    else:
        nbt = None
    
    item_new = item.upgrade(id, metadata, nbt)

    result = 'give ' + player + ' ' + item_new + ' '

    if 'count' in props:
        result += str(props['count'])

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)