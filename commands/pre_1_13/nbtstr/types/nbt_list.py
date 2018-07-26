from . import NBTType
from ..serialization_params import SerializationParams


class NBTList(NBTType):

    def __init__(self, values):
        self.values = values
    
    @property
    def values(self) -> list:
        return self.__values
    
    @values.setter
    def values(self, values: list):
        self.__values = values
    
    def __str__(self):
        if self.values:
            return '[{}]'.format(','.join([str(x) for x in self.values]))
        else:
            return '[]'
    
    def __eq__(self, other):
        # TODO Should we allow comparison of integer arrays and lists?
        if type(other) is not NBTList:
            return False
        
        return self.values == other.values