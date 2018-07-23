from ..command import Command, TargetSelector
from utils import CharStream, Tokenizer
from .commands import tellraw, testfor


# Dict values are functions like parse(tokenizer: Tokenizer, command: Command)
COMMAND_PARSERS = {
    'tellraw': tellraw.parse,
    'testfor': testfor.parse,
}

def parse_command(raw):
    if type(raw) is str:
        stream = CharStream(raw)
        tokenizer = Tokenizer(stream, True)
    elif type(raw) is CharStream:
        stream = raw
        tokenizer = Tokenizer(stream, True)
    elif type(raw) is Tokenizer:
        stream = raw.stream
        tokenizer = raw
    else:
        raise Exception('Unknown raw type')

    result = Command()

    tokenizer.expect_char('/', True)

    command_name = tokenizer.expect_alnum_word(['_'])

    if command_name in COMMAND_PARSERS:
        result.name = command_name
        COMMAND_PARSERS[command_name](tokenizer, result)
    else:
        raise Exception('Unknown command name: \'{}\''.format(command_name))

    return result