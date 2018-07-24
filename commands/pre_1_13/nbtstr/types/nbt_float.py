from . import NBTType


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
    
    def serialize(self) -> str:
        if self.size:
            return str(self.value) + self.size
        else:
            return str(self.value)
    
    def __str__(self):
        return '<NBTFloat {}{}>'.format(self.value, self.size if self.size else '')
