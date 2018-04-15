'''
Test Matcher matches with '*' operator and Boolean flag
'''
from __future__ import unicode_literals
from __future__ import print_function
import pytest

from ...matcher import Matcher
from ...vocab import Vocab
from ...attrs import LOWER
from ...tokens import Doc


def test_basic_case():
    matcher = Matcher(Vocab(
                lex_attr_getters={LOWER: lambda string: string.lower()}))
    IS_ANY_TOKEN = matcher.vocab.add_flag(lambda x: True)
    matcher.add_pattern(
        "FarAway",
        [
            {LOWER: "bob"},
            {'OP': '*', LOWER: 'and'},
            {LOWER: 'frank'}
        ])
    doc = Doc(matcher.vocab, words=['bob', 'and', 'and', 'frank'])
    match = matcher(doc)
    assert len(match) == 1
    ent_id, label, start, end = match[0]
    assert start == 0
    assert end == 4


@pytest.mark.xfail
def test_issue850():
    '''The problem here is that the variable-length pattern matches the
    succeeding token. We then don't handle the ambiguity correctly.'''
    matcher = Matcher(Vocab(
                lex_attr_getters={LOWER: lambda string: string.lower()}))
    IS_ANY_TOKEN = matcher.vocab.add_flag(lambda x: True)
    matcher.add_pattern(
        "FarAway",
        [
            {LOWER: "bob"},
            {'OP': '*', IS_ANY_TOKEN: True},
            {LOWER: 'frank'}
        ])
    doc = Doc(matcher.vocab, words=['bob', 'and', 'and', 'frank'])
    match = matcher(doc)
    assert len(match) == 1
    ent_id, label, start, end = match[0]
    assert start == 0
    assert end == 4
