class ID(object):

    def __init__(self, namespace, value):
        self.namespace = namespace
        self.value = value
    
    def __str__(self):
        if self.namespace:
            return self.namespace + ':' + self.value
        else:
            return 'minecraft:' + self.value