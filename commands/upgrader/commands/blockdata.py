from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base


CMDEXS = [
    CMDEx('blockdata {coordinate:x} {coordinate:y} {coordinate:z} {nbtstr:nbt}'),
]

def __upgrade(order, props):
    result = 'data merge block '

    result += str(props['x']) + ' ' + str(props['y']) + ' ' + str(props['z']) + ' '

    # TODO Maybe upgrade NBT stuff?
    result += str(props['nbt'])

    return result

def upgrade(command: str):
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)