from . import NBTType
from ..serialization_params import SerializationParams


class NBTBoolean(NBTType):

    def __init__(self, value):
        self.value = value
    
    @property
    def value(self) -> bool:
        return self.__value
    
    @value.setter
    def value(self, value:bool):
        self.__value = value
    
    def __str__(self):
        if self.value:
            return 'true'
        else:
            return 'false'
    
    def __eq__(self, other):
        if type(other) is not NBTBoolean:
            return False
        
        return self.value == other.value