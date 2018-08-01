from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import block


CMDEXS = [
    CMDEx('fill {coordinate:x1} {coordinate:y1} {coordinate:z1} {coordinate:x2} {coordinate:y2} {coordinate:z2} {id:block}'),

    CMDEx('fill {coordinate:x1} {coordinate:y1} {coordinate:z1} {coordinate:x2} {coordinate:y2} {coordinate:z2} {id:block} {int:bdata}'),
    CMDEx('fill {coordinate:x1} {coordinate:y1} {coordinate:z1} {coordinate:x2} {coordinate:y2} {coordinate:z2} {id:block} {blockstate:bstate}'),

    CMDEx('fill {coordinate:x1} {coordinate:y1} {coordinate:z1} {coordinate:x2} {coordinate:y2} {coordinate:z2} {id:block} {int:bdata} replace {id:old_block}'),
    CMDEx('fill {coordinate:x1} {coordinate:y1} {coordinate:z1} {coordinate:x2} {coordinate:y2} {coordinate:z2} {id:block} {blockstate:bstate} replace {id:old_block}'),

    CMDEx('fill {coordinate:x1} {coordinate:y1} {coordinate:z1} {coordinate:x2} {coordinate:y2} {coordinate:z2} {id:block} {int:bdata} replace {id:old_block} {int:old_data}'),
    CMDEx('fill {coordinate:x1} {coordinate:y1} {coordinate:z1} {coordinate:x2} {coordinate:y2} {coordinate:z2} {id:block} {blockstate:bstate} replace {id:old_block} {int:old_data}'),

    CMDEx('fill {coordinate:x1} {coordinate:y1} {coordinate:z1} {coordinate:x2} {coordinate:y2} {coordinate:z2} {id:block} {int:bdata} {str:handling}'),
    CMDEx('fill {coordinate:x1} {coordinate:y1} {coordinate:z1} {coordinate:x2} {coordinate:y2} {coordinate:z2} {id:block} {blockstate:bstate} {str:handling}'),

    CMDEx('fill {coordinate:x1} {coordinate:y1} {coordinate:z1} {coordinate:x2} {coordinate:y2} {coordinate:z2} {id:block} {int:bdata} {str:handling} {nbtstr:nbt}'),
    CMDEx('fill {coordinate:x1} {coordinate:y1} {coordinate:z1} {coordinate:x2} {coordinate:y2} {coordinate:z2} {id:block} {blockstate:bstate} {str:handling} {nbtstr:nbt}'),
]

def __upgrade(order, props):
    result = ''

    if len(order) >= 10 and order[9] == 'replace':
        new_id, new_state, new_nbt = block.upgrade(props['block'], props['bstate'] if 'bstate' in props else None, props['bdata'] if 'bdata' in props else None, None)
        old_id, old_state, old_nbt = block.upgrade(props['old_block'], None, props['old_data'] if 'old_data' in props else None, None)

        result += 'fill ' + str(props['x1']) + ' ' + str(props['y1']) + ' ' + str(props['z1']) + ' '
        result += str(props['x2']) + ' ' + str(props['y2']) + ' ' + str(props['z2']) + ' '

        result += str(new_id)
        if new_state:
            result += '[' + str(new_state) + ']'
        result += ' replace ' + str(old_id)
        if old_state:
            result += '[' + str(old_state) + ']'
        result += ' '
    else:
        new_id, new_state, new_nbt = block.upgrade(props['block'], props['bstate'] if 'bstate' in props else None, props['bdata'] if 'bdata' in props else None, props['nbt'] if 'nbt' in props else None)
        result += 'fill ' + str(props['x1']) + ' ' + str(props['y1']) + ' ' + str(props['z1']) + ' '
        result += str(props['x2']) + ' ' + str(props['y2']) + ' ' + str(props['z2']) + ' '
        result += str(new_id)
        if new_state:
            result += '[' + str(new_state) + ']'
        if new_nbt:
            result += str(new_nbt)
        result += ' '
        if 'handling' in props:
            result += props['handling'] + ' '
        if result[-1] == ' ':
            result = result[:-1]

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)