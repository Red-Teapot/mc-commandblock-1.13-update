from . import NBTType


class NBTValueType(NBTType):
    value_types = [type(None)]

    def __init__(self, value):
        super().__init__()

        self.value = value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if type(value) not in self.value_types:
            raise TypeError('Value type must be one of {}, not {}'.format(
                [str(x.__name__) for x in self.value_types], 
                str(type(value).__name__))
            )
        
        self.__value = value
    
    def __eq__(self, other):
        if type(other) in self.value_types:
            return self.value == other
        
        if type(other) is not type(self):
            return False
        
        return self.value == other.value
    
    def __str__(self):
        return str(self.value)