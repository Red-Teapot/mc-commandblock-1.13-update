from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector

CMDEXS = [
    CMDEx('function {function:function}'),
    CMDEx('function {function:function} if {selector:selector}'),
    CMDEx('function {function:function} unless {selector:selector}'),
]

def __upgrade(order, props):
    result = 'function ' + props['function'] + ' '

    if len(order) >= 3:
        if order[2] in ['if', 'unless']:
            result += order[2] + ' '
        result += selector.upgrade(props['selector']) + ' '
    
    if result[-1] == ' ':
        result = result[:-1]

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)