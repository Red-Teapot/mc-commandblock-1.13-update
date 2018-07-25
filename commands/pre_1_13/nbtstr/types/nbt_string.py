from . import NBTType


class NBTString(NBTType):
    
    def __init__(self, value):
        self.value = value
    
    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value
    
    def serialize(self) -> str:
        if not self.value:
            return '""'
        
        add_quotes = False
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
        return '<NBTString {}>'.format(self.serialize())