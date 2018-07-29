from . import NBTContainerType
from ..serialization_params import SerializationParams


class NBTIntegerArray(NBTContainerType):
    value_types = [list, type(None)]

    def __init__(self, size, value):
        super().__init__(value)

        self.size = size
    
    @property
    def size(self) -> str:
        return self.__size
    
    @size.setter
    def size(self, size: str):
        self.__size = (size.upper() if type(size) is str else size)
    
    # Kept for compatibility
    @property
    def values(self) -> list:
        return self.value
    
    @values.setter
    def values(self, values: list):
        self.value = values
    
    def __str__(self):
        if not self.value:
            return '[{};]'.format(self.size)
        else:
            return '[{};{}]'.format(self.size, ','.join([str(x) for x in self.value]))
    
    def __eq__(self, other):
        if type(other) is NBTIntegerArray:
            if self.size != other.size:
                return False
        
        return super().__eq__(other)