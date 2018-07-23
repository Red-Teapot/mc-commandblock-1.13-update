class TargetSelector(object):
    def __init__(self, variable=None, arguments=None, scores=None):
        self.variable = variable if variable else None
        self.arguments = arguments if arguments else dict()
        self.scores = scores if scores else dict()
    
    def __str__(self):
        result = '@'

        result += str(self.variable)

        if len(self.arguments) > 0 or len(self.scores) > 0:
            result += '['

            for name, value in self.arguments.items():
                result += '{}={},'.format(name, value)
            
            for name, value in self.scores.items():
                if 'min' in value:
                    result += 'score_{}_min={},'.format(name, value['min'])
                if 'val' in value:
                    result += 'score_{}={},'.format(name, value['val'])
            
            if result[-1] == ',':
                result = result[:-1]

            result += ']'

        return '<TargetSelector \'{}\'>'.format(result)