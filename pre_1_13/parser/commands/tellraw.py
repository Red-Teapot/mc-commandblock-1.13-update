import json

from pre_1_13 import Command, TargetSelector
from ..target_selector_parser import parse_target_selector
from utils import CharStream, Tokenizer, parse_alnum_word, consume_spaces


def parse(tokenizer: Tokenizer, command: Command):
    if tokenizer.expect_char('@', optional=True, pop=False):
        selector = parse_target_selector(tokenizer.stream)
    else:
        selector = tokenizer.expect_alnum_word(['_', '#', '.'])
    
    data = tokenizer.expect_json()

    tokenizer.skip_spaces()

    if len(tokenizer.stream.get_rest()) > 0:
        raise Exception('Unknown arguments: \'{}\''.format(tokenizer.stream.get_rest()))

    command.args = [selector, data]
    