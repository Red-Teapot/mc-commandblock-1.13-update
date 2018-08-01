from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import item, selector


CMDEXS = [
    CMDEx('replaceitem block {coordinate:x} {coordinate:y} {coordinate:z} {str:slot} {id:item}'),
    CMDEx('replaceitem block {coordinate:x} {coordinate:y} {coordinate:z} {str:slot} {id:item} {int:amount}'),
    CMDEx('replaceitem block {coordinate:x} {coordinate:y} {coordinate:z} {str:slot} {id:item} {int:amount} {int:data}'),
    CMDEx('replaceitem block {coordinate:x} {coordinate:y} {coordinate:z} {str:slot} {id:item} {int:amount} {int:data} {nbtstr:nbt}'),

    CMDEx('replaceitem entity {selector:selector} {str:slot} {id:item}'),
    CMDEx('replaceitem entity {selector:selector} {str:slot} {id:item} {int:amount}'),
    CMDEx('replaceitem entity {selector:selector} {str:slot} {id:item} {int:amount} {int:data}'),
    CMDEx('replaceitem entity {selector:selector} {str:slot} {id:item} {int:amount} {int:data} {nbtstr:nbt}'),
]

def __upgrade(order, props):
    result = 'replaceitem '

    if order[1] == 'block':
        result += 'block ' + str(props['x']) + ' ' + str(props['y']) + ' ' + str(props['z']) + ' '
    else:
        result += 'entity ' + selector.upgrade(props['selector']) + ' '
    
    slot = props['slot']

    if slot.startswith('slot.'):  # Cut the `slot.` part as it is incorrect in 1.13
        slot = slot[5:]
    
    result += slot + ' '

    result += item.upgrade(props['item'], props['data'] if 'data' in props else None, props['nbt'] if 'nbt' in props else None) + ' '

    if 'amount' in props:
        result += str(props['amount']) + ' '
    
    if result[-1] == ' ':
        result = result[:-1]

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)