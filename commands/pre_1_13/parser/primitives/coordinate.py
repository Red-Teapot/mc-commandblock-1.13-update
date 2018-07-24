class Coordinate(object):

    def __init__(self, prefix, value):
        self.prefix = prefix
        self.value = value
    
    def __str__(self):
        if self.prefix:
            strval = self.prefix + '' + str(self.value)
        else:
            strval = str(self.value)
        
        return '<Coordinate {}>'.format(strval)