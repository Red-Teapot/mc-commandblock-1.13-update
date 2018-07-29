from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base, selector, item


CMDEXS = [
    CMDEx('clear'),
    CMDEx('clear {selector:target}'),
    CMDEx('clear {selector:target} {id:item}'),
    CMDEx('clear {selector:target} {id:item} {int:data}'),
    CMDEx('clear {selector:target} {id:item} {int:data} {int:count}'),
    CMDEx('clear {selector:target} {id:item} {int:data} {int:count} {nbtstr:nbt}'),
]

def __upgrade(order, props):
    result = 'clear '

    if 'target' in props:
        new_selector = selector.upgrade(props['target'])
        result += str(new_selector) + ' '
    
    # TODO Maybe we need special handling for colored items: wool, carpets, beds, etc.
    if 'item' in props:
        id = props['item']
        data = props['data'] if 'data' in props else None
        nbt = props['nbt'] if 'nbt' in props else None

        new_item = item.upgrade(props['item'], data, nbt)

        result += str(new_item) + ' '
    
    if 'count' in props:
        count = props['count']
        result += str(count) + ' '
    
    if result[-1] == ' ':
        result = result[:-1]
    
    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)