from . import NBTType


class NBTList(NBTType):

    def __init__(self, values):
        self.values = values
    
    @property
    def values(self) -> list:
        return self.__values
    
    @values.setter
    def values(self, values: list):
        self.__values = values
    
    def serialize(self) -> str:
        if self.values:
            return '[{}]'.format(','.join([NBTType.serialize_val(x) for x in self.values]))
        else:
            return '[]'
    
    def __str__(self):
        if not self.values:
            return '<NBTList (no values)>'
        
        return '<NBTList {}>'.format(self.serialize())