from ..utils import selector
from commands.pre_1_13.cmdex import CMDEx
from commands.pre_1_13.nbtstr import SerializationParams


cmdexs = [
    CMDEx('testfor {selector:selector}'),
    CMDEx('testfor {selector:selector} {nbtstr:nbt}'),
]

ser_params = SerializationParams()

def upgrade(command: str) -> str:
    try:
        order, props = cmdexs[0].match(command)
        sel = selector.upgrade(props['selector'])
        return 'execute if entity {}'.format(sel)
    except: pass
    
    try:
        order, props = cmdexs[1].match(command)
        selector_old = props['selector']
        sel = selector.upgrade(selector_old, {'nbt': props['nbt'].serialize(ser_params)})
        return 'execute if entity {}'.format(sel)
    except: pass
    
    raise Exception('Unknown testfor command: \'{}\''.format(command))