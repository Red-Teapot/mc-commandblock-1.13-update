class CharStream(object):
    raw = ''
    idx = 0

    def __init__(self, raw):
        self.raw = raw
    
    def peek(self):
        return self.raw[0]
    
    def pop(self):
        c = self.raw[0]
        self.raw = self.raw[1:]
        self.idx += 1
        return c

    def peek_word(self):
        result = ''

        for c in self.raw:
            if result:
                if c.isalnum():
                    result += c
                else:
                    break
            else:
                if c.isalnum():
                    result += c
        
        return result
    
    def pop_word(self):
        result = ''

        for c in self.raw:
            if result:
                if c.isalnum():
                    result += c
                else:
                    break
            else:
                if c.isalnum():
                    result += c
            
        self.raw = self.raw[len(result):]
        
        return result