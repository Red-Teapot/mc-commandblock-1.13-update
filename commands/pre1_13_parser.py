import re

VARIABLE_TYPES = ['p', 'r', 'a', 'e', 's']

class CharStream(object):
    raw = ''
    idx = 0

    def __init__(self, raw):
        self.raw = raw
    
    def peek(self):
        return self.raw[0]
    
    def pop(self):
        c = self.raw[0]
        self.raw = self.raw[1:]
        self.idx += 1
        return c

class TargetSelector(object):
    def __init__(self, variable=None, arguments=dict(), scores=dict()):
        self.variable = variable
        self.arguments = arguments
        self.scores = scores
    
    @staticmethod
    def parse(raw):
        state = 1

        result = TargetSelector()

        if type(raw) == str:
            stream = CharStream(raw)
        elif type(raw) == CharStream:
            stream = raw
        else:
            raise Exception('Unknown raw type')

        argname = ''
        argval = ''

        args = list()
        
        i = 0
        while True:
            if state == 1:  # Skip leading spaces
                if stream.peek() != ' ':
                    state = 2
                else:
                    stream.pop()
            
            if state == 2:  # Check for '@' char
                if stream.peek() == '@':
                    state = 3
                    stream.pop()
                else:
                    raise Exception('Wrong char at {}: \'{}\', expected \'@\''.format(i, stream.peek()))
            if state == 3:  # Read variable
                if stream.peek() in VARIABLE_TYPES:
                    result.variable = stream.peek()
                    stream.pop()
                    state = 4
                else:
                    raise Exception('Unknown variable type: \'{}\', must be one of {}'.format(stream.peek(), VARIABLE_TYPES))
            
            if state == 4:  # Check if selector ends here
                if len(stream.raw) == 0:
                    return result
                else:
                    state = 5
            
            if state == 5:  # Begin reading selector arguments
                if stream.peek() == '[':
                    state = 6
                    stream.pop()
                else:
                    raise Exception('Wrong char at {}: \'{}\', expected \'[\''.format(i, stream.peek()))

            if state == 6:  # Try to find ']' char or continue to read arguments
                if stream.peek() == ']':
                    stream.pop()
                    break
                else:
                    state = 7
            
            if state == 7:  # Read argument name
                if stream.peek().isalnum() or stream.peek() == '_':
                    argname += stream.peek()
                    stream.pop()
                elif stream.peek() == '=':
                    state = 8
                    stream.pop()
                else:
                    raise Exception('Wrong char at {}: \'{}\''.format(i, stream.peek()))
            
            if state == 8:  # Read argument value
                if stream.peek().isalnum() or stream.peek() in ['_', '!', '#', '-']:
                    argval += stream.peek()
                    stream.pop()
                elif stream.peek() == ',' or stream.peek() == ']':
                    state = 9
                else:
                    raise Exception('Wrong char at {}: \'{}\''.format(i, stream.peek()))
            
            if state == 9:  # Add argument to list and reset stuff
                args += [(argname, argval)]
                argname = ''
                argval = ''

                if stream.peek() == ',':
                    state = 6
                    stream.pop()
                elif stream.peek() == ']':
                    stream.pop()
                    break

            i += 1
        
        for name, value in args:
            if name.startswith('score_'):
                is_min = name.endswith('_min')
                name_clean = name[len('score_'):-len('_min') if is_min else None]

                if name_clean not in result.scores:
                    result.scores[name_clean] = dict()

                if is_min:
                    result.scores[name_clean]['min'] = value
                else:
                    result.scores[name_clean]['val'] = value
            else:
                result.arguments[name] = value
        
        return result
    
    def __str__(self):
        return '<Selector @' + self.variable + '; ' + str(self.arguments) + '; ' + str(self.scores) + '>'

class Pre_1_13_Parser(object):
    pass