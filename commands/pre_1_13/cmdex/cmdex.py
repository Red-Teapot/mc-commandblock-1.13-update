from ..parser.tokenizer import Tokenizer


# CMDEx source format: {} {} ...
# Where {} is a token. Token format:
# `{type:name}`` or `word`
# First will match token of type `type` and place it under the name `name`
# Second will match that exact word and fail otherwise
# Token types: str, float, int, json, nbtstr, selector, id, blockstate, coordinate, * (will catch the rest of a command)

class CMDEx(object):

    def __init__(self, source: str):
        tokens = list()

        src_split = source.split(' ')
        for tok in src_split:
            if tok[0] == '{' and tok[-1] == '}':
                tok = tok[1:-1]
                tok_split = tok.split(':')
                tok_type = tok_split[0]
                tok_name = tok_split[1]

                tokens += [(tok_type, tok_name)]
            else:
                tokens += [tok]
        
        self.tokens = tokens
    
    def match(self, cmd: str) -> list:
        tokenizer = Tokenizer(cmd)

        order = list()
        props = dict()

        for token in self.tokens:
            if len(tokenizer.source[tokenizer.pos:].lstrip()) == 0:  # Expected token, but command is too short
                raise Exception('Command is too short, expected {}'.format(token))
            
            if type(token) is str:
                tokenizer.expect_specific_word(token)
                
                order += [token]
            else:
                exp_type = token[0]
                name = token[1]

                if exp_type == 'str':
                    val = tokenizer.read_word(lambda x: x.isalnum() or x in '_-.#!', lambda x: x == ' ', lambda x: x == ' ', pop=True)
                elif exp_type == 'op':
                    val = tokenizer.read_word(lambda x: x in '+-></*=%', lambda x: x == ' ', lambda x: x == ' ', pop=True)
                elif exp_type == 'tag':
                    val = tokenizer.read_word(lambda x: x != ' ', lambda x: x == ' ', lambda x: x == ' ', pop=True)
                elif exp_type == 'function':
                    val = tokenizer.read_word(lambda x: x.isalnum() or x in '_:/.', lambda x: x == ' ', lambda x: x == ' ', pop=True)
                elif exp_type == 'float':
                    val = tokenizer.expect_float()
                elif exp_type == 'int':
                    val = tokenizer.expect_integer()
                elif exp_type == 'json':
                    val = tokenizer.expect_json()
                elif exp_type == 'nbtstr':
                    val = tokenizer.expect_nbtstr()
                elif exp_type == 'selector':
                    val = tokenizer.expect_selector()
                elif exp_type == 'id':
                    val = tokenizer.expect_id()
                elif exp_type == 'blockstate':
                    val = tokenizer.expect_blockstate()
                elif exp_type == 'coordinate':
                    val = tokenizer.expect_coordinate()
                elif exp_type == '*':
                    val = tokenizer.source[tokenizer.pos:]

                    if val[0] == ' ':
                        val = val[1:]
                    
                    tokenizer.pos = len(tokenizer.source)
                else:
                    raise Exception('Unknown token type: {}'.format(exp_type))
                
                order += ['#' + name]
                props[name] = val
        
        if len(tokenizer.source[tokenizer.pos:].lstrip()) != 0:  # Expected end of command, but found stuff
                raise Exception('Command is too long, unexpected \'{}\''.format(tokenizer.source[tokenizer.pos:]))
        
        return order, props
    
    def __str__(self):
        result = ''

        for tok in self.tokens:
            if type(tok) is str:
                result += tok + ' '
            else:
                result += '{' + tok[0] + ':' + tok[1] + '} '
        
        if result[-1] == ' ':
            result = result[:-1]
        
        return result