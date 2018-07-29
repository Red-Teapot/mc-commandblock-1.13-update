from . import NBTValueType
from ..serialization_params import SerializationParams


class NBTInteger(NBTValueType):
    value_types = [int]

    def __init__(self, size, value):
        super().__init__(value)

        self.size = size
    
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
    
    def __str__(self):
        size = self.size
        
        if size:
            return str(self.value) + size
        else:
            return str(self.value)
    
    def __eq__(self, other):
        if type(other) is NBTInteger:
            if self.size != other.size:
                return False
        
        return super().__eq__(other)