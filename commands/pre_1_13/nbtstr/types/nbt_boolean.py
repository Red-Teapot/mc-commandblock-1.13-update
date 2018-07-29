from . import NBTValueType
from ..serialization_params import SerializationParams


class NBTBoolean(NBTValueType):
    value_types = [bool]

    def __init__(self, value):
        super().__init__(value)
    
    def __str__(self):
        if self.value:
            return 'true'
        else:
            return 'false'
    
    def __bool__(self):
        return self.value