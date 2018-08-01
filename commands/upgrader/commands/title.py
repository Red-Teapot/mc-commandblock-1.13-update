import json
from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector


CMDEXS = [
    CMDEx('title {selector:player} title {json:title}'),
    CMDEx('title {selector:player} subtitle {json:title}'),
    CMDEx('title {selector:player} actionbar {json:title}'),
    CMDEx('title {selector:player} clear'),
    CMDEx('title {selector:player} reset'),
    CMDEx('title {selector:player} times {int:fade_in} {int:stay} {int:fade_out}'),
]

def __upgrade(order, props):
    result = 'title ' + selector.upgrade(props['player']) + ' '

    result += order[2] + ' '

    if order[2] in ['title', 'subtitle', 'actionbar']:
        result += json.dumps(props['title'], ensure_ascii=False) + ' '
    elif order[2] == 'times':
        result += str(props['fade_in']) + ' ' + str(props['stay']) + ' ' + str(props['fade_out']) + ' '
    
    if result[-1] == ' ':
        result = result[:-1]

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)