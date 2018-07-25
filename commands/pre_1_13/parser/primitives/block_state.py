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