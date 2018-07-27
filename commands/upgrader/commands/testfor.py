from ..utils import selector
from commands.pre_1_13.cmdex import CMDEx
from commands.pre_1_13.nbtstr import SerializationParams
from commands.upgrader.utils import command_upgrader_base


CMDEXS = [
    CMDEx('testfor {selector:selector}'),
    CMDEx('testfor {selector:selector} {nbtstr:nbt}'),
]

def __upgrade(order, props):
    if 'nbt' in props:
        selector_old = props['selector']
        sel = selector.upgrade(selector_old, {'nbt': str(props['nbt'])})
        return 'execute if entity {}'.format(sel)
    else:
        sel = selector.upgrade(props['selector'])
        return 'execute if entity {}'.format(sel)

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)