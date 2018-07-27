class BlockState(object):

    def __init__(self, data):
        self.data = data
    
    def __str__(self):
        result = ''

        for k, v in self.data.items():
            result += str(k) + '=' + str(v) + ','
        
        if result and result[-1] == ',':
            result = result[:-1]
        
        return result
    
    def __eq__(self, other):
        # TODO Allow comparison of BlockStates and dicts?
        if type(other) is not BlockState:
            return False
        
        return self.data == other.data
    
    @staticmethod
    def parse(src: str):
        data = dict()
        if src:
            for tok in src.split(','):
                k, v = tok.split('=')

                data[k] = v
        return BlockState(data)