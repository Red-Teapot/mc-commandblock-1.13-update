from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector, nbt


CMDEXS = [
    CMDEx('entitydata {selector:entity} {nbtstr:data}'),
]

def __upgrade(order, props):
    new_selector = selector.upgrade(props['entity'], {'limit': 1})
    result = 'data merge entity ' + new_selector + ' ' + str(nbt.entity.upgrade(props['data'])) + ' '
    if result[-1] == ' ':
        return result[:-1]
    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)