from json import JSONDecoder, JSONDecodeError

from . import CharStream, UnexpectedCharException


json_decoder = JSONDecoder()

class Tokenizer(object):
    
    def __init__(self, stream: CharStream, auto_skip_spaces=True):
        self.stream = stream
        self.auto_skip_spaces = auto_skip_spaces
    
    def skip_spaces(self):
        while self.stream.peek() == ' ':
            self.stream.pop()
    
    def expect_char(self, char: str, optional=False, pop=True):
        if len(char) != 1:
            raise TypeError('Length of char argument must be 1')
        
        if self.auto_skip_spaces:
            self.skip_spaces()
        
        if self.stream.peek() == char:
            if pop:
                self.stream.pop()
            return True
        elif not optional:
            raise UnexpectedCharException(self.stream.idx, self.stream.peek(), char, self.stream.raw)
        
        return False
    
    def expect_alnum_word(self, extra_allowed_chars=[]):
        if self.auto_skip_spaces:
            self.skip_spaces()
        
        result = ''

        while True:
            c = self.stream.peek()

            if c.isalnum() or c in extra_allowed_chars:
                result += c
                self.stream.pop()
            else:
                break
        
        return result
    
    def expect_json(self, optional=False, pop=True):
        if self.auto_skip_spaces:
            self.skip_spaces()
        
        tail = self.stream.get_rest()

        try:
            data, length = json_decoder.raw_decode(tail)
        except JSONDecodeError as e:
            if not optional:
                e.pos += self.stream.idx
                raise e
        
        if pop:
            self.stream.idx += length
        
        return data
    
    def expect_end(self):
        self.skip_spaces()

        if len(self.stream.get_rest()) > 0:
            raise Exception('Unknown arguments: \'{}\''.format(self.stream.get_rest()))
    