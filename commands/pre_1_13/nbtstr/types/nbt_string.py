from . import NBTContainerType
from ..serialization_params import SerializationParams


class NBTString(NBTContainerType):
    value_types = [str, type(None)]
    
    def __init__(self, value, had_quotes=False):
        super().__init__(value)
        self.had_quotes = had_quotes
    
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