from . import selector
from commands.pre_1_13.parser.tokenizer import Tokenizer


def upgrade(json_text) -> dict:
    if type(json_text) in [str, float, int, bool, None]:
        return json_text
    elif type(json_text) is list:
        return [upgrade(x) for x in json_text]
    elif type(json_text) is dict:
        text = json_text.copy()

        if 'selector' in text:
            tokenizer = Tokenizer(text['selector'])
            sel = tokenizer.expect_selector(pop=True)
            text['selector'] = selector.upgrade(sel)
        if 'score' in text and 'name' in text['score']:
            tokenizer = Tokenizer(text['score']['name'])
            sel = tokenizer.expect_selector(pop=True)
            text['score']['name'] = selector.upgrade(sel)
        if 'extra' in text:
            extra = text['extra']
            for i in range(0, len(extra)):
                extra[i] = upgrade(extra[i])

        return text
    else:
        raise Exception('Unknown JSON text type: {}'.format(type(json_text)))