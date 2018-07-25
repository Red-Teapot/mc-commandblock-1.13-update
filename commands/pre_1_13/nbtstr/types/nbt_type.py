from ..serialization_params import SerializationParams

class NBTType(object):
    default_serialization_params = SerializationParams()

    def serialize(self, serialization_params: SerializationParams) -> str:
        raise NotImplementedError()
    
    @staticmethod
    def serialize_val(val, serialization_params: SerializationParams) -> str:
        if isinstance(val, NBTType):
            return val.serialize(serialization_params)
        else:
            return str(val)
