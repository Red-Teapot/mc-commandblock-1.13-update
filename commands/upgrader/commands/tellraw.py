import json
from ..utils import selector
from commands.pre_1_13.cmdex import CMDEx
from commands.upgrader.utils import json_text


cmdex = CMDEx('tellraw {selector:selector} {json:message}')

def upgrade(command: str) -> str:
    order, props = cmdex.match(command)

    new_selector = selector.upgrade(props['selector'])

    new_message = json_text.upgrade(props['message'])

    return 'tellraw {} {}'.format(new_selector, json.dumps(new_message, ensure_ascii=False))