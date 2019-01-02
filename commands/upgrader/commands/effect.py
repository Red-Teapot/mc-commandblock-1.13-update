from commands.pre_1_13.cmdex import CMDEx
from commands.pre_1_13.parser.primitives import ID
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector, effect


CMDEXS = [
    CMDEx('effect {selector:player} clear'),

    CMDEx('effect {selector:player} {int:id}'),
    CMDEx('effect {selector:player} {int:id} {int:duration}'),
    CMDEx('effect {selector:player} {int:id} {int:duration} {int:amplifier}'),
    CMDEx('effect {selector:player} {int:id} {int:duration} {int:amplifier} true'),
    CMDEx('effect {selector:player} {int:id} {int:duration} {int:amplifier} false'),

    CMDEx('effect {selector:player} {id:id}'),
    CMDEx('effect {selector:player} {id:id} {int:duration}'),
    CMDEx('effect {selector:player} {id:id} {int:duration} {int:amplifier}'),
    CMDEx('effect {selector:player} {id:id} {int:duration} {int:amplifier} true'),
    CMDEx('effect {selector:player} {id:id} {int:duration} {int:amplifier} false'),
]

def __upgrade(order, props):
    # Hack to handle clear command
    if order[2] == 'clear':
        return 'effect clear ' + selector.upgrade(props['player'])
    
    new_selector = selector.upgrade(props['player'])

    new_id = effect.upgrade(props['id'].value if type(props['id']) is ID else props['id'])

    if type(props['id']) is ID:
        new_id = props['id']
        new_id.value = effect.upgrade(new_id.value)
    else:
        new_id = ID(None, effect.upgrade(props['id']))

    if 'duration' in props and props['duration'] <= 0:
        result = 'effect clear ' + new_selector + ' ' + str(new_id)
    else:
        result = 'effect give ' + new_selector + ' ' + str(new_id) + ' '

        if 'duration' in props:
            result += str(props['duration']) + ' '
        
        if 'amplifier' in props:
            result += str(props['amplifier']) + ' '
        
        if len(order) == 6 and order[5] in ['true', 'false']:
            result += order[5] + ' '
    
    if result[-1] == ' ':
        result = result[:-1]

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)