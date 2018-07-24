from json import JSONDecoder

from .primitives.id import ID
from .primitives.coordinate import Coordinate
from .primitives.selector import Selector


json_decoder = JSONDecoder()
allowed_selector_variables = ['p', 'e', 'a', 'r', 's']
selector_arguments = {
    'x': int, 'y': int, 'z': int,
    'dx': int, 'dy': int, 'dz': int,
    'r': int, 'rm': int,
    'tag': str, 'team': str,
    'c': int,
    'l': int, 'lm': int,
    'm': str,
    'name': str,
    'rx': int, 'rxm': int,
    'ry': int, 'rym': int,
    'type': str,
}

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
                arguments[name] = selector_arguments[name](value)
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
    
    def expect_alnum_word(self, pop=True) -> str:
        return self.read_word(lambda x: x.isalnum(), lambda x: x == ' ', lambda x: x == ' ', pop=pop)
    
    def expect_integer(self, pop=True) -> int:
        return int(self.read_word(lambda x: x.isdigit(), lambda x: x == ' ', lambda x: x == ' ', pop=pop))

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
        word = self.read_word(lambda x: x.isalnum() or x in ['_', ':'], lambda x: x == ' ', lambda x: x == ' ', pop=pop)

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
    
    def expect_coordinate(self, pop=True) -> Coordinate:
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
            elif c == ' ':
                break
            else:
                raise Exception('Unknown char at {}: \'{}\''.format(pos, c))
            
            pos += 1
        
        if pop:
            self.pos = pos
        
        if '.' in value_str:
            value = float(value_str)
        else:
            value = int(value_str)
        
        return Coordinate(prefix, value)

    def expect_json(self, pop=True) -> dict:
        result, pos = json_decoder.raw_decode(self.source[self.pos:])

        if pop:
            self.pos += pos
        
        return result
    
    def expect_selector(self, pop=True):
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
                
                # Read value
                while True:
                    c = self.char(pos)

                    if c.isalnum() or c in ['_', ':', '.', '#', '-', '!']:
                        argval += c
                    elif c == ',':
                        pos += 1
                        break
                    elif c == ']':
                        break
                    else:
                        raise Exception('Unknown char at {}: \'{}\''.format(pos, self.char(pos)))
                    
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
                
                if c.isalnum() or c in ['.', '_', '#']:
                    result += c
                elif c == ' ':
                    break
                else:
                    raise Exception('Unknown char at {}: \'{}\''.format(pos, c))
                
                pos += 1
        
        if pop:
            self.pos = pos
        
        return result

    def expect_nbtstr(self, pop=True):
        # TODO Parser for NBT strings?
        raise NotImplementedError()
