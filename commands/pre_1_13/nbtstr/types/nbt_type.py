class NBTType(object):

    def serialize(self) -> str:
        raise NotImplementedError()
    
    @staticmethod
    def serialize_val(val) -> str:
        if isinstance(val, NBTType):
            return val.serialize()
        else:
            return str(val)
