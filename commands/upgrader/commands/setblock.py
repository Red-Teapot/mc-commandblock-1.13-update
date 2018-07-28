import logging

from commands.pre_1_13.cmdex import CMDEx
from commands.pre_1_13.nbtstr import SerializationParams
from commands.upgrader.utils import block, command_upgrader_base
from commands import upgrader

logger = logging.getLogger(__name__)

CMDEXS = [
    CMDEx('setblock {coordinate:x} {coordinate:y} {coordinate:z} {id:id}'),

    CMDEx('setblock {coordinate:x} {coordinate:y} {coordinate:z} {id:id} {blockstate:state}'),
    CMDEx('setblock {coordinate:x} {coordinate:y} {coordinate:z} {id:id} {blockstate:state} {str:handling}'),
    CMDEx('setblock {coordinate:x} {coordinate:y} {coordinate:z} {id:id} {blockstate:state} {str:handling} {nbtstr:nbt}'),

    CMDEx('setblock {coordinate:x} {coordinate:y} {coordinate:z} {id:id} {int:data}'),
    CMDEx('setblock {coordinate:x} {coordinate:y} {coordinate:z} {id:id} {int:data} {str:handling}'),
    CMDEx('setblock {coordinate:x} {coordinate:y} {coordinate:z} {id:id} {int:data} {str:handling} {nbtstr:nbt}'),
]

def __upgrade(order, props):
    if 'handling' in props and props['handling'] not in ['destroy', 'keep', 'replace']:
        raise Exception('Unknown old block handling mode: {}'.format(props['handling']))
        
    id = props['id']

    if 'data' in props:
        data = props['data']
    else:
        data = None
    
    if 'state' in props:
        state = props['state']
    else:
        state = None
    
    if 'nbt' in props:
        nbt = props['nbt']
    else:
        nbt = None
    
    new_id, new_state, new_nbt = block.upgrade(id, state, data, nbt)

    if new_id.value == 'command_block':
        if new_nbt and new_nbt.values and 'Command' in new_nbt.values:
            new_nbt.values['Command'].value = upgrader.upgrade(new_nbt.values['Command'].value)

    block_val = str(new_id)

    if new_state:
        block_val += '[' + str(new_state) + ']'
    
    if new_nbt:
        block_val += str(new_nbt)
        
    handling = ''
    if 'handling' in props:
        handling = props['handling']
    
    return 'setblock {} {} {} {} {}'.format(props['x'], props['y'], props['z'], block_val, handling).strip()

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)