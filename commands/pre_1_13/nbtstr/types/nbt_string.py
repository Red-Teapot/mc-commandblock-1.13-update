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
        
        value = self.value.replace('"', '\\"')

        return '"' + value + '"'