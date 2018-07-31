from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import command_upgrader_base
from commands import upgrader
from ..utils import selector, block

CMDEXS = [
    CMDEx('execute {selector:selector} {coordinate:x} {coordinate:y} {coordinate:z} {*:command}'),

    CMDEx('execute {selector:selector} {coordinate:x} {coordinate:y} {coordinate:z} detect {coordinate:bx} {coordinate:by} {coordinate:bz} {id:block} {int:bdata} {*:command}'),
    CMDEx('execute {selector:selector} {coordinate:x} {coordinate:y} {coordinate:z} detect {coordinate:bx} {coordinate:by} {coordinate:bz} {id:block} {blockstate:bstate} {*:command}'),
]

def __upgrade(order, props):
    result = 'execute '

    selector_new = selector.upgrade(props['selector'])

    result += 'as ' + selector_new + ' at @s '

    if str(props['x']) != '~' or str(props['y']) != '~' or str(props['z']) != '~':
        result += 'positioned ' + str(props['x']) + ' ' + str(props['y']) + ' ' + str(props['z']) + ' '

    if order[5] == 'detect':
        result += 'if block ' + str(props['bx']) + ' ' + str(props['by']) + ' ' + str(props['bz']) + ' '
        block_new = None
        if 'bdata' in props:
            block_new = block.upgrade(props['block'], None, props['bdata'], None)
        else:
            block_new = block.upgrade(props['block'], props['bstate'], None, None)
        result += str(block_new[0])
        if block_new[1]:
            result += '[' + str(block_new[1]) + ']'
        if block_new[2]:
            result += str(block_new[2])
        result += ' '
    
    new_cmd = upgrader.upgrade(props['command'])
    if new_cmd[0] == '/':
        new_cmd = new_cmd[1:]
    
    result += 'run ' + new_cmd

    return result

def upgrade(command: str) -> str:
    return command_upgrader_base.upgrade(CMDEXS, command, __upgrade)