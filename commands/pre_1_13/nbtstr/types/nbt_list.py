from . import NBTType


class NBTList(NBTType):

    def __init__(self, values):
        self.values = values
    
    @property
    def values(self) -> list:
        return self.__values
    
    @values.setter
    def values(self, values: list):
        self.__values = values
    
    def __serialize_member(self, member) -> str:
        if hasattr(member, 'serialize'):
            return member.serialize()
        else:
            return str(member)
    
    def serialize(self) -> str:
        if self.values:
            return '[{}]'.format(','.join([self.__serialize_member(x) for x in self.values]))
        else:
            return '[]'
    
    def __str__(self):
        if not self.values:
            return '<NBTList (no values)>'
        
        return '<NBTList {}>'.format(self.serialize())