import json
from ..utils import selector
from commands.pre_1_13.cmdex import CMDEx


cmdex = CMDEx('tellraw {selector:selector} {json:message}')

def upgrade(command: str) -> str:
    order, props = cmdex.match(command)

    new_selector = selector.upgrade(props['selector'])

    return 'tellraw {} {}'.format(new_selector, json.dumps(props['message'], ensure_ascii=False))