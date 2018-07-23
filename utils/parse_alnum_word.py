from . import CharStream


def parse_alnum_word(stream: CharStream, allowed_chars=list()):
    result = ''

    while True:
        if stream.peek().isalnum() or stream.peek() in allowed_chars:
            result += stream.peek()
            stream.pop()
        elif stream.peek() == ' ':
            break
        else:
            raise Exception('Wrong char at {}: \'{}\'; expected alphanumeric'.format(stream.idx + 1, stream.peek()))
    
    return result