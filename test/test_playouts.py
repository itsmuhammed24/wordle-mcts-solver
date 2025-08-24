import unittest
from wordle import WordleState
from playouts import (
    random_playout,
    entropy_playout,
    frequency_playout,
    entropy_plus_playout,
    frequency_plus_playout,
)

class TestPlayouts(unittest.TestCase):
    def setUp(self):
        # Mini dictionnaire de test
        self.wordlist = ["apple", "grape", "peach", "melon", "berry"]
        self.secret = "apple"

    def test_random_playout(self):
        state = WordleState(self.secret)
        result = random_playout(state, self.wordlist)
        self.assertIn(result, [0.0, 1.0])

    def test_entropy_playout(self):
        state = WordleState(self.secret)
        result = entropy_playout(state, self.wordlist)
        self.assertIn(result, [0.0, 1.0])

    def test_frequency_playout(self):
        state = WordleState(self.secret)
        result = frequency_playout(state, self.wordlist)
        self.assertIn(result, [0.0, 1.0])

    def test_entropy_plus_playout(self):
        state = WordleState(self.secret)
        result = entropy_plus_playout(state, self.wordlist)
        self.assertIn(result, [0.0, 1.0])

    def test_frequency_plus_playout(self):
        state = WordleState(self.secret)
        result = frequency_plus_playout(state, self.wordlist)
        self.assertIn(result, [0.0, 1.0])


if __name__ == "__main__":
    unittest.main()
