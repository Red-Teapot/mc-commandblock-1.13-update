from . import NBTContainerType
from ..serialization_params import SerializationParams


class NBTCompound(NBTContainerType):
    value_types = [dict, type(None)]

    def __init__(self, value):
        super().__init__(value)
    
    # Kept for compatibility
    @property
    def values(self) -> dict:
        return self.value
    
    @values.setter
    def values(self, values: dict):
        self.value = values
    
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
