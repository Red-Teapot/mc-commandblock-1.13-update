class SerializationParams(object):

    def __init__(self, string_quote_mode='auto', integer_suffix_mode='auto', float_suffix_mode='auto', default_integer_suffix='L', key_quote_mode='auto'):
        self.string_quote_mode = string_quote_mode
        self.integer_suffix_mode = integer_suffix_mode
        self.float_suffix_mode = float_suffix_mode
        self.default_integer_suffix = default_integer_suffix
        self.key_quote_mode = key_quote_mode
    
    @property
    def string_quote_mode(self) -> str:
        return self.__string_quote_mode
    
    @string_quote_mode.setter
    def string_quote_mode(self, mode: str):
        if mode not in ['auto', 'force', 'preserve']:
            raise TypeError('Mode must be one of [auto, force, preserve]')
        
        self.__string_quote_mode = mode
    
    @property
    def integer_suffix_mode(self) -> str:
        return self.__integer_suffix_mode
    
    @integer_suffix_mode.setter
    def integer_suffix_mode(self, mode: str):
        if mode not in ['auto', 'force']:
            raise TypeError('Mode must be one of [auto, force]')
        
        self.__integer_suffix_mode = mode
    
    @property
    def float_suffix_mode(self) -> str:
        return self.__float_suffix_mode
    
    @float_suffix_mode.setter
    def float_suffix_mode(self, mode: str):
        if mode not in ['auto', 'force']:
            raise TypeError('Mode must be one of [auto, force]')
        
        self.__float_suffix_mode = mode
    
    @property
    def default_integer_suffix(self) -> str:
        return self.__default_integer_suffix
    
    @default_integer_suffix.setter
    def default_integer_suffix(self, suffix: str):
        if suffix not in 'BbSsLl':
            raise TypeError('Suffix must be one of [B, S, L]')
        
        self.__default_integer_suffix = suffix
    
    @property
    def key_quote_mode(self) -> str:
        return self.__key_quote_mode
    
    @key_quote_mode.setter
    def key_quote_mode(self, mode: str):
        if mode not in ['auto', 'force']:
            raise TypeError('Mode must be one of [auto, force]')
        
        self.__key_quote_mode = mode