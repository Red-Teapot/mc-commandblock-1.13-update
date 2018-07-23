class CharStream(object):
    def __init__(self, raw):
        self.raw = raw
        self.idx = 0
    
    def peek(self):
        return self.raw[self.idx]
    
    def pop(self):
        result = self.raw[self.idx]
        self.idx += 1
        return result
    
    def peek_alnum_word(self, allowed_chars=list()):
        result = ''

        i = self.idx
        while i < len(self.raw):
            c = self.raw[i]
            if c.isalnum() or c in allowed_chars:
                result += c
            else:
                break
            
            i += 1
        
        return result
    
    def get_rest(self):
        return self.raw[self.idx:]