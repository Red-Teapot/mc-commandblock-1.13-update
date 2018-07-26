from . import NBTType
from ..serialization_params import SerializationParams


class NBTCompound(NBTType):

    def __init__(self, values):
        self.values = values
    
    @property
    def values(self) -> dict:
        return self.__values
    
    @values.setter
    def values(self, values: dict):
        self.__values = values
    
    def __str__(self):
        if not self.values:
            return '{}'
        
        result = '{'
        
        for key, value in self.values.items():
            quote = False

            if not quote:
                for c in ' {}[],:':
                    if c in key:
                        quote = True
                        break
            
            if quote:
                key = '"' + key + '"'
            
            result += key + ':'

            result += str(value)
            
            result += ','
        
        if result[-1] == ',':
            result = result[:-1]
        
        result += '}'

        return result
    
    def __eq__(self, other):
        if type(other) is not NBTCompound:
            return False
        
        return self.values == other.values