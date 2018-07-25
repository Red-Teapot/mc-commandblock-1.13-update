class Selector(object):

    def __init__(self, variable, arguments, scores):
        self.variable = variable
        self.arguments = arguments
        self.scores = scores
    
    def __str__(self):
        result = '@' + self.variable

        have_args = False
        if self.arguments and len(self.arguments) > 0:
            have_args = True
        if self.scores and len(self.scores) > 0:
            have_args = True
        
        if have_args:
            result += '['
        
            for key, value in self.arguments.items():
                result += (key + '=' + str(value) + ',')
            
            for key, value in self.scores.items():
                if 'min' in value:
                    result += ('score_' + key + '_min=' + str(value['min']) + ',')
                if 'max' in value:
                    result += ('score_' + key + '=' + str(value['max']) + ',')
            
            if result[-1] == ',':
                result = result[:-1]
            
            result += ']'
        
        return result
