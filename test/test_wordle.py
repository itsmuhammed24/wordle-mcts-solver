import pytest
from wordle import WordleState
from playouts import (
    random_playout,
    entropy_playout,
    frequency_playout,
    entropy_plus_playout,
    frequency_plus_playout,
)


@pytest.fixture
def wordlist():
    return ["apple", "grape", "melon", "peach", "berry"]


@pytest.fixture
def state(wordlist):
    return WordleState(secret="apple", max_attempts=6)


def test_random_playout(state, wordlist):
    result = random_playout(state, wordlist)
    assert result in [0.0, 1.0]


def test_entropy_playout(state, wordlist):
    result = entropy_playout(state, wordlist)
    assert result in [0.0, 1.0]


def test_frequency_playout(state, wordlist):
    result = frequency_playout(state, wordlist)
    assert result in [0.0, 1.0]


def test_entropy_plus_playout(state, wordlist):
    result = entropy_plus_playout(state, wordlist)
    assert result in [0.0, 1.0]


def test_frequency_plus_playout(state, wordlist):
    result = frequency_plus_playout(state, wordlist)
    assert result in [0.0, 1.0]
