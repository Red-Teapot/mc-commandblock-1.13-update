class UnexpectedCharException(Exception):

    def __init__(self, pos, found, expected, src=None):
        self.pos = pos
        self.found = found
        self.expected = expected
        self.src = src
    
    def __str__(self):
        if type(self.expected) is str:
            return 'Unexpected char at {}: \'{}\'; expected \'{}\''.format(self.pos, self.found, self.expected)
        elif type(self.expected) is list:
            return 'Unexpected char at {}: \'{}\'; expected one of [{}]'.format(self.pos, self.found, ', '.join(self.expected))
        else:
            return 'Unexpected char at {}: \'{}\''.format(self.pos, self.found)
