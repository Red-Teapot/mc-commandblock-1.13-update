from ..command import Command, TargetSelector
from utils import CharStream


COMMAND_PARSERS = {

}

def parse_command(raw):
    if type(raw) == str:
        stream = CharStream(raw)
    elif type(raw) == CharStream:
        stream = raw
    else:
        raise Exception('Unknown raw type')
    
    state = 1

    result = Command()

    i = 0
    while True:
        if state == 1:  # Check for leading slash or comment sign and skip leading spaces
            if stream.peek() == '/':
                state = 2
                stream.pop()
            elif stream.peek() == ' ':
                stream.pop()
            elif stream.peek().isalnum():
                state = 2
            else:
                raise Exception('Wrong char at {}: \'{}\', expected \'/\' or a letter'.format(i, stream.peek()))
        
        if state == 2:  # Parse actual command
            if stream.peek().isalnum():
                command_name = stream.peek_word()
                
                if command_name in COMMAND_PARSERS:
                    COMMAND_PARSERS[command_name](stream, result)
                else:
                    raise Exception('Unknown command name: \'{}\''.format(command_name))

                break
            else:
                raise Exception('Wrong char at {}: \'{}\', expected a letter'.format(i, stream.peek()))
        
        i += 1

    return result