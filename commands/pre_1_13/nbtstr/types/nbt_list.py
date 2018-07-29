from . import NBTContainerType
from ..serialization_params import SerializationParams


class NBTList(NBTContainerType):
    value_types = [list, type(None)]

    def __init__(self, value):
        self.value = value
    
    # Kept for compatibility
    @property
    def values(self) -> list:
        return self.value
    
    @values.setter
    def values(self, values: list):
        self.value = values
    
    def __str__(self):
        if self.values:
            return '[{}]'.format(','.join([str(x) for x in self.values]))
        else:
            return '[]'
