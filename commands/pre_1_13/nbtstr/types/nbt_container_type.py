from . import NBTValueType


class NBTContainerType(NBTValueType):
    
    def __init__(self, value):
        super().__init__(value)
    
    def __len__(self):
        if self.value:
            return len(self.value)
        else:
            return 0
    
    def __contains__(self, value):
        if self.value:
            if type(value) is type(self):
                return value.value in self.value
            else:
                return value in self.value
        else:
            return False
    
    def __getitem__(self, key):
        if self.value:
            return self.value[key]
        else:
            raise KeyError()
    
    def __delitem__(self, key):
        if self.value:
            del self.value[key]
        else:
            raise KeyError()
    
    def __setitem__(self, key, value):
        if self.value:
            self.value[key] = value
        else:
            raise KeyError()
    
    def __iter__(self):
        if self.value:
            return self.value.__iter__()
        else:
            raise Exception('Value is not set')
