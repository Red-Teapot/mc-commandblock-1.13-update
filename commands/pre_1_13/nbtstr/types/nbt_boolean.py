from . import NBTType


class NBTBoolean(NBTType):

    def __init__(self, value):
        self.value = value
    
    @property
    def value(self) -> bool:
        return self.__value
    
    @value.setter
    def value(self, value:bool):
        self.__value = value
    
    def serialize(self) -> str:
        if self.value:
            return 'true'
        else:
            return 'false'
    
    def __str__(self):
        return '<NBTBoolean {}>'.format(self.serialize())