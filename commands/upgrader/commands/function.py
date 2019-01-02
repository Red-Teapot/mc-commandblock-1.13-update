from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector

CMDEXS = [
    CMDEx('function {function:function}'),
    CMDEx('function {function:function} if {selector:selector}'),
    CMDEx('function {function:function} unless {selector:selector}'),
]

def __upgrade(order, props):
    result = ''

    colon_idx = props['function'].index(':')
    function = 'default:' + props['function'][:colon_idx] + '/' + props['function'][colon_idx+1:]

    if len(order) >= 3:
        result += 'execute '
        result += order[2] + ' entity '
        result += selector.upgrade(props['selector']) + ' '
        result += 'run function '
        result += function
    else:
        result += 'function ' + function
    
    if result[-1] == ' ':
        result = result[:-1]

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)