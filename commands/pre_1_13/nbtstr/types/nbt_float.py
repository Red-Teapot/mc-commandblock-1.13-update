from . import NBTType
from ..serialization_params import SerializationParams


class NBTFloat(NBTType):

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
        
        if size not in 'FDfd':
            raise Exception('Size must be one of [F, D]')
        
        self.__size = size.upper()
    
    @property
    def value(self) -> float:
        return self.__value
    
    @value.setter
    def value(self, value: float):
        self.__value = value
    
    def __str__(self):
        size = self.size
        
        if size:
            return str(self.value) + size
        else:
            return str(self.value)
    
    def __eq__(self, other):
        # TODO Should we allow comparison of NBTFloats and NBTIntegers?
        if type(other) is not NBTFloat:
            return False
        
        # TODO Should we ignore the size?
        return self.value == other.value
