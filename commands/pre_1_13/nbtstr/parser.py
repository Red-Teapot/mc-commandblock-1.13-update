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

            if c.isalnum() or c in '._+-':
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
                if size:
                    val += size
        
        if val[-1].isdigit() or val[-1] in 'FDfd':  # Try to get float
            size = None
            if val[-1] in 'FDfd':
                size = val[-1]
                val = val[:-1]
            try:
                return NBTFloat(size, float(val))
            except: 
                if size:
                    val += size
        
        return NBTString(val, False)
    
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
        
        return NBTString(val, True)

    def __parse_key(self) -> str:  # Compound key (string or alnum with ._+-, no spaces or stuff)
        if self.get(self.pos) == '"':  # Key is wrapped in quotes
            return self.__parse_string().value

        val = ''

        while True:
            c = self.get(self.pos)

            if not c:
                break

            if c.isalnum() or c in '._+-':
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
            if self.get(self.pos) == '}':
                self.pos += 1
                break
            
            key = self.__parse_key()

            if self.get(self.pos) != ":":
                raise Exception('Unknown char at {}:\'{}\', expected \'{}\''.format(self.pos, self.get(self.pos), ':'))
            
            self.pos += 1

            value = self.__parse_node()

            values[key] = value

            if self.get(self.pos) == ',':
                self.pos += 1
        
        return NBTCompound(values)

    def __parse_integer_array(self) -> NBTIntegerArray:
        if self.get(self.pos) != '[':
            raise Exception('Unknown char at {}:\'{}\', expected \'{}\''.format(self.pos, self.get(self.pos), '['))
        
        self.pos += 1

        size = self.get(self.pos).upper()

        if size not in 'BbIiLl':
            raise Exception('Unknown array type: \'{}\' at {}'.format(self.get(self.pos), self.pos))
        
        self.pos += 1

        if self.get(self.pos) != ';':
            raise Exception('Unknown char at {}:\'{}\', expected \'{}\''.format(self.pos, self.get(self.pos), ';'))
        
        self.pos += 1
        
        values = list()

        while True:
            if self.get(self.pos) == ']':
                self.pos += 1
                break
            
            old_pos = self.pos

            val = self.__parse_primitive()

            if type(val) is not NBTInteger:
                raise Exception('Unknown primitive type at {}: {}, expected NBTInteger'.format(self.pos, type(val).__name__))
            
            if size == 'I' and val.size:
                raise Exception('Wrong integer type at {}: {}, expected {}'.format(old_pos, val.size, size))
            
            if size != 'I' and size != val.size:
                raise Exception('Wrong integer type at {}: {}, expected {}'.format(old_pos, val.size, size))
            
            values += [val]

            c = self.get(self.pos)

            if c == ',':
                self.pos += 1
            elif c != ']':
                raise Exception('Unknown char at {}:\'{}\', expected , or ]'.format(self.pos, self.get(self.pos)))
        
        return NBTIntegerArray(size, values)

    def __parse_list(self) -> NBTList:
        if self.get(self.pos) != '[':
            raise Exception('Unknown char at {}:\'{}\', expected \'{}\''.format(self.pos, self.get(self.pos), '['))
        
        self.pos += 1

        val_type = None
        values = list()

        while True:
            if self.get(self.pos) == ']':
                self.pos += 1
                break
            
            old_pos = self.pos

            val = self.__parse_node()

            if not val_type:
                val_type = type(val)
                values += [val]
            elif val_type == type(val):
                values += [val]
            else:
                raise Exception('Unknown node type at {}: {}, expected {}'.format(old_pos, type(val).__name__, val_type.__name__))
            
            if self.get(self.pos) == ',':
                self.pos += 1
            elif self.get(self.pos) != ']':
                raise Exception('Unknown char at {}:\'{}\', expected \'{}\''.format(self.pos, self.get(self.pos), ','))
        
        return NBTList(values)

    def __parse_node(self) -> NBTType:
        # Try to figure out base type
        c = self.source[self.pos]

        if c == '{':  # Compound
            return self.__parse_compound()
        elif c == '[':  # List or array
            if self.get(self.pos + 2) == ';':  # Integer array
                return self.__parse_integer_array()
            else:
                return self.__parse_list()
        elif c == '"':  # String
            return self.__parse_string()
        else:  # Boolean, integer, float or string
            return self.__parse_primitive()
    
    def parse(self, source: str) -> NBTType:
        self.source = source.lstrip()
        self.pos = 0

        if not self.source:
            return None

        return self.__parse_node()
