from ..pre_1_13.cmdex import CMDEx
from .commands import tellraw


def dummy(command: str) -> str:
    return command

CMD_UPGRADERS = {
    'tellraw': tellraw.upgrade,
}

def upgrade(command: str) -> str:
    command = command.strip()

    if command[0] == '/':
        command = command[1:]
    
    name = command[:command.find(' ')]

    if name in CMD_UPGRADERS:
        return CMD_UPGRADERS[name](command)
    else:
        # TODO Maybe a warning?
        return command