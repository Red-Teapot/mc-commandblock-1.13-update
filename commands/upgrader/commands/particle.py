from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from commands.upgrader.data import particle_id_map

CMDEXS = [
    CMDEx('particle {str:name} {*:rest}'),
]

def __upgrade(order, props):
    result = 'particle '
    name = props['name']
    if name in particle_id_map:
        result += particle_id_map[name]
    else:
        result += name
    result += ' '
    if name == 'reddust':
        result += '1 0 0 1 '
    result += props['rest']
    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)