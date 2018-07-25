class Coordinate(object):

    def __init__(self, prefix, value):
        self.prefix = prefix
        self.value = value
    
    def __str__(self):
        if self.prefix:
            if self.value:
                return self.prefix + str(self.value)
            else:
                return self.prefix
        else:
            if self.value:
                return str(self.value)
            else:
                return '0'