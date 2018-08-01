from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector


CMDEXS = [
    CMDEx('spreadplayers {coordinate:x} {coordinate:z} {int:spread} {int:range} {str:respect_teams} {selector:players}'),
]

def __upgrade(order, props):
    result = 'spreadplayers ' + str(props['x']) + ' ' + str(props['z']) + ' '
    result += str(props['spread']) + ' '
    result += str(props['range']) + ' '
    result += str(props['respect_teams']) + ' '
    result += selector.upgrade(props['players'])
    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)