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
    
    def serialize(self, serialization_params: SerializationParams) -> str:
        if not self.value:
            return '""'
        
        add_quotes = False
        
        # Follow ser. params
        if serialization_params.string_quote_mode == 'force':
            add_quotes = True
        elif serialization_params.string_quote_mode == 'preserve':
            add_quotes = self.had_quotes
        
        # Don't allow to serialize incorrectly
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
    
    def __str__(self):
        return '<NBTString {}>'.format(self.serialize(NBTType.default_serialization_params))