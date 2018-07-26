from . import NBTType
from ..serialization_params import SerializationParams


class NBTString(NBTType):
    
    def __init__(self, value, had_quotes=False):
        self.value = value
        self.had_quotes = had_quotes
    
    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value
    
    def __str__(self):
        if not self.value:
            return '""'
        
        add_quotes = False
        
        if not add_quotes:
            for c in self.value:
                if not c.isalnum() and c not in '._+-':
                    add_quotes = True
                    break
        
        value = self.value.replace('"', '\\"')
        if add_quotes:
            return '"' + value + '"'
        else:
            return value
    
    def __eq__(self, other):
        if type(other) is not NBTString:
            return False
        
        return self.value == other.value