from json import JSONDecoder

from .primitives import ID
from .primitives import Coordinate
from .primitives import Selector
from .primitives import BlockState
from .. import nbtstr
from ..nbtstr.types import NBTType


json_decoder = JSONDecoder()
allowed_selector_variables = ['p', 'e', 'a', 'r', 's']
selector_arguments = [
    'x', 'y', 'z',
    'dx', 'dy', 'dz',
    'r', 'rm',
    'tag', 'team',
    'c',
    'l', 'lm',
    'm',
    'name',
    'rx', 'rxm',
    'ry', 'rym',
    'type',
]
nbtstr_parser = nbtstr.Parser()

def process_selector_arguments(args: list) -> dict:
    scores = dict()
    arguments = dict()

    for name, value in args:
        if name.startswith('score_'):
            name = name[6:]

            min = name.endswith('_min')
            if min:
                name = name[:-4]
            
            if name not in scores:
                scores[name] = dict()

            if min:
                scores[name]['min'] = value
            else:
                scores[name]['max'] = value
        else:
            if name in selector_arguments:
                arguments[name] = value
            else:
                raise Exception('Unknown selector argument: {}={}'.format(name, value))
    
    return arguments, scores

class Tokenizer(object):

    def __init__(self, source: str):
        self.source = source
        self.length = len(self.source)
        self.pos = 0
    
    def char(self, pos) -> str:
        if pos < self.length:
            return self.source[pos]
        else:
            return None

    def move(self, delta=1):
        self.pos += delta
    
    def read_char(self, pop=False) -> str:
        if self.pos < self.length:
            if pop:
                self.pos += 1
            return self.source[self.pos]
        else:
            return None
    
    def read_word(self, check_word: callable, check_end: callable, check_pre: callable, pop=False) -> str:
        pos = self.pos

        result = ''
    
        while True:
            c = self.char(pos)

            if not check_pre(c):
                break
            
            pos += 1

        while True:
            c = self.char(pos)

            if not c:
                break

            if check_word(c):
                result += c
            elif check_end(c):
                break
            else:
                raise Exception('Unknown char at {}: \'{}\''.format(pos, c))
            
            pos += 1
        
        if pop:
            self.pos = pos
        
        return result
    
    def expect_alnum_word(self, pop=True, stop_chars=' ') -> str:
        return self.read_word(lambda x: x.isalnum(), lambda x: x in stop_chars, lambda x: x == ' ', pop=pop)
    
    def expect_integer(self, pop=True, stop_chars=' ') -> int:
        return int(self.read_word(lambda x: x.isdigit() or x in '+-', lambda x: x in stop_chars, lambda x: x == ' ', pop=pop))

    def expect_float(self, pop=True) -> float:
        pos = self.pos

        result_str = ''

        while True:
            if self.char(pos) != ' ':
                break
            
            pos += 1

        read_dot = False

        if self.char(pos) == '-':
            result_str += '-'
            pos += 1
        
        while True:
            c = self.char(pos)

            if not c:
                break

            if c == '.':
                if read_dot:
                    raise Exception('Unknown dot at {}'.format(pos))
                else:
                    result_str += '.'
                    read_dot = True
            elif c.isdigit():
                result_str += c
            elif c == ' ':
                break
            else:
                raise Exception('Unknown char at {}: \'{}\''.format(pos, c))
            
            pos += 1
        
        if pop:
            self.pos = pos
        
        return float(result_str)
    
    def expect_id(self, pop=True) -> ID:
        pos = self.pos
        word = self.read_word(lambda x: x.isalnum() or x in ['_', ':', '!'], lambda x: x in [' ', ',', ']'], lambda x: x == ' ', pop=pop)

        if word.count(':') > 1:
            self.pos = pos
            raise Exception('Too many \':\' chars in ID at {}'.format(self.pos))
        
        if ':' in word:
            tokens = word.split(':')

            if not tokens[0]:
                self.pos = pos
                raise Exception('Empty namespace is not allowed at {}'.format(self.pos))
            
            if not tokens[1]:
                self.pos = pos
                raise Exception('Empty value is not allowed at {}'.format(self.pos))
            
            return ID(tokens[0], tokens[1])
        else:
            return ID(None, word)
    
    def expect_coordinate(self, pop=True, stop_chars=' ') -> Coordinate:
        pos = self.pos

        value_str = ''
        prefix = None

        while True:
            if self.char(pos) != ' ':
                break
            
            pos += 1

        read_dot = False

        if self.char(pos) in ['~', '^']:
            prefix = self.char(pos)
            pos += 1

        if self.char(pos) == '-':
            value_str += '-'
            pos += 1
        
        while True:
            c = self.char(pos)

            if not c:
                break

            if c == '.':
                if read_dot:
                    raise Exception('Unknown dot at {}'.format(pos))
                else:
                    value_str += '.'
                    read_dot = True
            elif c.isdigit():
                value_str += c
            elif c in stop_chars:
                break
            else:
                raise Exception('Unknown char at {}: \'{}\''.format(pos, c))
            
            pos += 1
        
        if pop:
            self.pos = pos
        
        if value_str:
            if '.' in value_str:
                value = float(value_str)
            else:
                value = int(value_str)
        else:
            value = None
        
        return Coordinate(prefix, value)

    def expect_json(self, pop=True) -> dict:
        pos = self.pos
        while True:
            c = self.char(pos)

            if c != ' ':
                break
            
            pos += 1
        
        result, pos_json = json_decoder.raw_decode(self.source[pos:])

        if pop:
            self.pos += pos + pos_json
        
        return result
    
    def expect_selector(self, pop=True) -> Selector:
        pos = self.pos

        while True:
            if self.char(pos) != ' ':
                break
            
            pos += 1
        
        if self.char(pos) == '@':
            pos += 1

            variable = self.char(pos)

            if variable not in allowed_selector_variables:
                raise Exception('Unknown selector variable at {}: \'{}\''.format(pos, variable))
            
            pos += 1

            if self.char(pos) == ' ' or not self.char(pos):
                pos += 1
                if pop:
                    self.pos = pos
                return Selector(variable, None, None)

            if self.char(pos) == '[':
                pos += 1
            else:
                raise Exception('Unknown char at {}: \'{}\''.format(pos, self.char(pos)))
            
            args = list()
            argname = ''
            argval = ''

            # Read key-value pair
            while True:
                if self.char(pos) == ']':
                    pos += 1
                    break
                
                argname = ''
                argval = ''
                
                # Read key
                while True:
                    c = self.char(pos)

                    if c.isalnum() or c in ['_']:
                        argname += c
                    elif c == '=':
                        pos += 1
                        break
                    else:
                        raise Exception('Unknown char at {}: \'{}\''.format(pos, self.char(pos)))
                    
                    pos += 1
                
                old_pos = self.pos
                self.pos = pos

                if argname in ['x', 'y', 'z', 'r', 'rm', 'dx', 'dy', 'dz', 'c', 'l', 'lm', 'rx', 'rxm', 'ry', 'rym'] or argname.startswith('score_'):
                    argval = self.expect_integer(stop_chars=' ,]')
                elif argname in ['tag', 'team', 'name', 'm']:
                    argval = self.read_word(lambda x: x.isalnum() or x in '_!.#', lambda x: x in ' ,]', lambda x: x == ' ', pop=pop)
                elif argname == 'type':
                    argval = self.expect_id(pop=pop)
                else:
                    raise Exception('Unknown selector argument: {}'.format(argname))

                pos = self.pos
                self.pos = old_pos

                if self.char(pos) == ',':
                    pos += 1
                
                args += [(argname, argval)]

            arguments, scores = process_selector_arguments(args)

            result = Selector(variable, arguments, scores)
        else:
            result = ''

            while True:
                c = self.char(pos)

                if not c:
                    break
                
                if c.isalnum() or c in '._#!':
                    result += c
                elif c == ' ':
                    break
                else:
                    raise Exception('Unknown char at {}: \'{}\''.format(pos, c))
                
                pos += 1
        
        if pop:
            self.pos = pos
        
        return result

    def expect_nbtstr(self, pop=True) -> NBTType:
        pos = self.pos
        while True:
            c = self.char(pos)

            if c != ' ':
                break
            
            pos += 1

        result, length = nbtstr_parser.parse(self.source[pos:])

        if pop:
            self.pos += length + pos

        return result

    def expect_blockstate(self, pop=True) -> BlockState:
        pos = self.pos

        while True:
            c = self.char(pos)

            if c != ' ':
                break
            
            pos += 1
        
        result = dict()

        while True:
            if not self.char(pos):
                break
            
            name = ''
            value = ''

            # Read name
            while True:
                c = self.char(pos)

                if not c:
                    raise Exception('Blockstate has no value, ended too early')

                if c.isalnum() or c in '_.-+:':
                    name += c
                elif c == '=':
                    pos += 1
                    break
                else:
                    raise Exception('Unknown char at {}: \'{}\''.format(pos, self.char(pos)))
                
                pos += 1
            
            # Read value
            while True:
                c = self.char(pos)

                if not c:
                    if value:
                        break
                    else:
                        raise Exception('Blockstate has no value, ended too early')
                
                if c.isalnum() or c in '_.-+:':
                    value += c
                elif c == ',':
                    break
                elif c == ' ':
                    break
                else:
                    raise Exception('Unknown char at {}: \'{}\''.format(pos, self.char(pos)))
                
                pos += 1
            
            result[name] = value

            if self.char(pos) == ',':
                pos += 1
            elif self.char(pos) == ' ':
                break
        
        if pop:
            self.pos = pos

        return BlockState(result)

    def expect_specific_word(self, word: str, stop_chars=' ', pop=True) -> bool:
        pos = self.pos

        while True:
            c = self.char(pos)

            if not c or c != ' ':
                break
            
            pos += 1

        for c in word:
            if c != self.char(pos):
                raise Exception('Unknown char at {}: \'{}\', expected \'{}\''.format(pos, self.char(pos), c))
            
            pos += 1
        
        if self.char(pos) and self.char(pos) not in stop_chars:
            raise Exception('Unknown char at {}: \'{}\', expected one of \'{}\''.format(pos, self.char(pos), stop_chars))
        
        if pop:
            self.pos = pos
        
        return True