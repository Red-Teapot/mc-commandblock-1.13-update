from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector


CMDEXS = [
    CMDEx('xp {str:amount} {selector:player}'),
]

def __upgrade(order, props):
    result = ''

    amount_raw = props['amount'].lower()

    is_levels = True if amount_raw[-1] == 'l' else False
    amount = int(amount_raw[:-1]) if is_levels else int(amount_raw)
    sel = selector.upgrade(props['player'])

    result += 'xp add '
    result += sel + ' '
    result += str(amount) + ' '
    result += 'levels ' if is_levels else 'points '

    if result[-1] == ' ':
        result = result[:-1]
    
    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)