class Selector(object):

    def __init__(self, variable, arguments, scores):
        self.variable = variable
        self.arguments = arguments
        self.scores = scores
    
    def __str__(self):
        strval = ''
        
        for key, value in self.arguments.items():
            strval += (key + '=' + str(value) + ',')
        
        for key, value in self.scores.items():
            if 'min' in value:
                strval += ('score_' + key + '_min=' + str(value['min']) + ',')
            if 'max' in value:
                strval += ('score_' + key + '=' + str(value['max']) + ',')
        
        if strval[-1] == ',':
            strval = strval[:-1]
        
        return '<Selector @{}[{}]>'.format(self.variable, strval)
