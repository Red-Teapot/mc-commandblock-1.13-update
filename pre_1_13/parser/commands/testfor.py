from pre_1_13 import Command, TargetSelector
from ..target_selector_parser import parse_target_selector
from utils import CharStream, Tokenizer


def parse(tokenizer: Tokenizer, command: Command):
    if tokenizer.expect_char('@', optional=True, pop=False):
        selector = parse_target_selector(tokenizer.stream)
    else:
        selector = tokenizer.expect_alnum_word(['_', '#', '.'])

    # TODO Parse NBT
    tokenizer.expect_end()

    command.args = [selector]