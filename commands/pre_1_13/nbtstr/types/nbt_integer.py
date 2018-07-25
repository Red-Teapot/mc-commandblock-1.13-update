from . import NBTType
from ..serialization_params import SerializationParams


class NBTInteger(NBTType):

    def __init__(self, size, value):
        self.size = size
        self.value = value
    
    @property
    def size(self) -> str:
        return self.__size
    
    @size.setter
    def size(self, size: str):
        if not size:
            self.__size = None
            return
        
        if size not in 'BSLbsl':
            raise TypeError('Size must be one of [B, S, L]')
        
        self.__size = size.upper()
    
    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, value: int):
        # TODO Maybe some range check?
        self.__value = value
    
    def serialize(self, serialization_params: SerializationParams) -> str:
        size = self.size

        if not size and serialization_params.integer_suffix_mode == 'force':
            size = serialization_params.default_integer_suffix
        
        if size:
            return str(self.value) + size
        else:
            return str(self.value)
    
    def __str__(self):
        return '<NBTInteger {}>'.format(self.serialize(NBTType.default_serialization_params))