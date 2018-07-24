from .types import NBTBoolean, NBTCompound, NBTFloat, NBTInteger, NBTIntegerArray, NBTList, NBTString, NBTType


class Parser(object):

    def __init__(self):
        pass
    
    def get(self, pos: int) -> str:
        if pos < len(self.source):
            return self.source[pos]
        else:
            return None
    
    def __parse_primitive(self) -> NBTType:
        val = ''

        while True:
            c = self.get(self.pos)

            if not c:
                break

            if c.isalnum() or c in '-._':
                val += c
            else:
                break
            
            self.pos += 1
        
        if val == 'true' or val == 'false':  # Boolean
            return NBTBoolean(val == 'true')
        
        if val[-1].isdigit() or val[-1] in 'BSLbsl':  # Try to get integer
            size = None
            if val[-1] in 'BSLbsl':
                size = val[-1]
                val = val[:-1]
            try:
                return NBTInteger(size, int(val))
            except: 
                val += size
        
        if val[-1].isdigit() or val[-1] in 'FDfd':  # Try to get float
            size = None
            if val[-1] in 'FDfd':
                size = val[-1]
                val = val[:-1]
            try:
                return NBTFloat(size, float(val))
            except: 
                val += size
        
        return NBTString(val)
    
    def __parse_string(self) -> NBTString:
        if self.get(self.pos) != '"':
            raise Exception('Unknown char at {}:\'{}\', expected \'{}\''.format(self.pos, self.get(self.pos), ':'))
        
        self.pos += 1

        val = ''

        while True:
            c = self.get(self.pos)

            if not c:
                break

            if c == '"':
                self.pos += 1
                break
            elif c == '\\' and self.get(self.pos + 1) == '"':
                val += '"'
                self.pos += 1
            else:
                val += c
            
            self.pos += 1
        
        return NBTString(val)

    def __parse_key(self) -> str:  # Compound key (string or alnum with _, no spaces or stuff)
        if self.get(self.pos) == '"':  # Key is wrapped in quotes
            return self.__parse_string().value

        val = ''

        while True:
            c = self.get(self.pos)

            if not c:
                break

            if c.isalnum() or c == '_':
                val += c
            else:
                break
            
            self.pos += 1
        
        return val

    def __parse_compound(self) -> NBTCompound:
        values = dict()

        if self.get(self.pos) != '{':
            raise Exception('Unknown char at {}:\'{}\', expected \'{}\''.format(self.pos, self.get(self.pos), '{'))
        
        self.pos += 1

        while True:
            key = self.__parse_key()

            if self.get(self.pos) != ":":
                raise Exception('Unknown char at {}:\'{}\', expected \'{}\''.format(self.pos, self.get(self.pos), ':'))
            
            self.pos += 1

            value = self.__parse_node()

            values[key] = value

            if self.get(self.pos) == '}':
                self.pos += 1
                break
            elif self.get(self.pos) == ',':
                self.pos += 1
        
        return NBTCompound(values)

    def __parse_node(self) -> NBTType:
        # Try to figure out base type
        c = self.source[self.pos]

        if c == '{':  # Compound
            return self.__parse_compound()
        elif c == '[':  # List or array
            print('List or array')
        elif c == '"':  # String
            return self.__parse_string()
        else:  # Boolean, integer, float or string
            return self.__parse_primitive()
    
    def parse(self, source: str) -> NBTType:
        self.source = source.strip()
        self.pos = 0

        return self.__parse_node()
        

def parse(source: str) -> NBTType:
    pass