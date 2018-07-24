class ID(object):

    def __init__(self, namespace, value):
        self.namespace = namespace
        self.value = value
    
    def __str__(self):
        if self.namespace:
            strval = self.namespace + ':' + self.value
        else:
            strval = self.value
        
        return '<ID \'{}\'>'.format(strval)