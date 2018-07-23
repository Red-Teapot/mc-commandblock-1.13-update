from . import CharStream


def consume_spaces(stream: CharStream):
    while stream.peek() == ' ':
        stream.pop()