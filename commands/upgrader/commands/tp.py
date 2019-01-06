from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from ..utils import selector


CMDEXS = [
    CMDEx('tp {selector:destination_player}'),
    CMDEx('tp {selector:target_player} {selector:destination_player}'),

    CMDEx('tp {coordinate:x} {coordinate:y} {coordinate:z}'),
    CMDEx('tp {selector:target_player} {coordinate:x} {coordinate:y} {coordinate:z}'),
    CMDEx('tp {selector:target_player} {coordinate:x} {coordinate:y} {coordinate:z} {int:yaw}'),
    CMDEx('tp {selector:target_player} {coordinate:x} {coordinate:y} {coordinate:z} {int:yaw} {int:pitch}'),
]

def __upgrade(order, props):
    if 'destination_player' in props:
        result = 'tp '
        if 'target_player' in props:
            result += selector.upgrade(props['target_player']) + ' '
        result += selector.upgrade(props['destination_player'])
        if result[-1] == ' ':
            result = result[:-1]
        return result
    else:
        result = ''

        if (props['x'].prefix or props['y'].prefix or props['z'].prefix) and 'target_player' in props:
            result += 'execute as '
            result += selector.upgrade(props['target_player']) + ' '
            result += 'at @s run tp @s '
            result += str(props['x']) + ' ' + str(props['y']) + ' ' + str(props['z']) + ' '
        else:
            result += 'tp '
            if 'target_player' in props:
                result += selector.upgrade(props['target_player']) + ' '
            result += str(props['x']) + ' ' + str(props['y']) + ' ' + str(props['z']) + ' '

        if 'yaw' in props:
            result += str(props['yaw']) + ' '
        if 'pitch' in props:
            result += str(props['pitch']) + ' '
        if result[-1] == ' ':
            result = result[:-1]
        return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)