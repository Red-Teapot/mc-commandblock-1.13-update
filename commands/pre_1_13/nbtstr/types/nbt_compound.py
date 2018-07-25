from . import NBTType


class NBTCompound(NBTType):

    def __init__(self, values):
        self.values = values
    
    @property
    def values(self) -> dict:
        return self.__values
    
    @values.setter
    def values(self, values: dict):
        self.__values = values
    
    def serialize(self) -> str:
        if not self.values:
            return '{}'
        
        result = '{'
        
        for key, value in self.values.items():
            for c in ' {}[],:':
                if c in key:
                    key = '"' + key + '"'
                    break
            
            result += key + ':'

            result += NBTType.serialize_val(value)
            
            result += ','
        
        if result[-1] == ',':
            result = result[:-1]
        
        result += '}'

        return result
    
    def __str__(self):
        return '<NBTCompound {}>'.format(self.serialize())