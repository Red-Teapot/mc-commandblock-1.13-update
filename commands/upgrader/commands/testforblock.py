from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import block


CMDEXS = [
    CMDEx('testforblock {coordinate:x} {coordinate:y} {coordinate:z} {id:block}'),

    CMDEx('testforblock {coordinate:x} {coordinate:y} {coordinate:z} {id:block} *'),
    CMDEx('testforblock {coordinate:x} {coordinate:y} {coordinate:z} {id:block} -1'),
    CMDEx('testforblock {coordinate:x} {coordinate:y} {coordinate:z} {id:block} {int:bdata}'),
    CMDEx('testforblock {coordinate:x} {coordinate:y} {coordinate:z} {id:block} {blockstate:bstate}'),

    CMDEx('testforblock {coordinate:x} {coordinate:y} {coordinate:z} {id:block} * {nbtstr:nbt}'),
    CMDEx('testforblock {coordinate:x} {coordinate:y} {coordinate:z} {id:block} -1 {nbtstr:nbt}'),
    CMDEx('testforblock {coordinate:x} {coordinate:y} {coordinate:z} {id:block} {int:bdata} {nbtstr:nbt}'),
    CMDEx('testforblock {coordinate:x} {coordinate:y} {coordinate:z} {id:block} {blockstate:bstate} {nbtstr:nbt}'),
]

def __upgrade(order, props):
    result = 'execute if block '

    result += str(props['x']) + ' ' + str(props['y']) + ' ' + str(props['z']) + ' '

    new_id, new_state, new_nbt = block.upgrade(props['block'], props['bstate'] if 'bstate' in props else None, props['bdata'] if 'bdata' in props else None, props['nbt'] if 'nbt' in props else None)

    result += str(new_id)
    if new_state:
        result += '[' + str(new_state) + ']'
    if new_nbt:
        result += str(new_nbt)
    result += ' '

    if result[-1] == ' ':
        result = result[:-1]

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)