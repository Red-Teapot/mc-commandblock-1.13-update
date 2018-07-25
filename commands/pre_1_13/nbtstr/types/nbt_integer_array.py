from . import NBTType
from ..serialization_params import SerializationParams


class NBTIntegerArray(NBTType):

    def __init__(self, size, values):
        self.size = size
        self.values = values
    
    @property
    def size(self) -> str:
        return self.__size
    
    @size.setter
    def size(self, size: str):
        self.__size = size
    
    @property
    def values(self) -> list:
        return self.__values
    
    @values.setter
    def values(self, values: list):
        self.__values = values
    
    def serialize(self, serialization_params: SerializationParams) -> str:
        if not self.values:
            return '[{};]'.format(self.size)
        else:
            return '[{};{}]'.format(self.size, ','.join([NBTType.serialize_val(x, serialization_params) for x in self.values]))
    
    def __str__(self):
        return '<NBTIntegerArray {}>'.format(self.serialize(NBTType.default_serialization_params))