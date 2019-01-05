from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector


CMDEXS = [
    CMDEx('gc help'),
    CMDEx('gc reload'),

    CMDEx('gc fulllevelup {selector:player}'),
    CMDEx('gc resetinfo {selector:player}'),

    CMDEx('gc getclan {selector:player}'),
    CMDEx('gc getguild {selector:player}'),
    CMDEx('gc getlevel {selector:player}'),

    CMDEx('gc gotoguild {selector:player} {str:guild}'),
    CMDEx('gc setclan {selector:player} {str:clan}'),
    CMDEx('gc setguild {selector:player} {str:guild}'),
    CMDEx('gc setlevel {selector:player} {int:level}'),
]

def __upgrade(order, props):
    result = ''

    for tok in order:
        if tok[0] == '#':
            key = tok[1:]
            if key == 'player':
                result += selector.upgrade(props[key]) + ' '
            else:
                result += str(props[key]) + ' '
        else:
            result += tok + ' '
    
    if result[-1] == ' ':
        result = result[:-1]

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)