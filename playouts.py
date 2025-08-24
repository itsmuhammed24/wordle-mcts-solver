import random
import math
from collections import Counter
from wordle import WordleState


# ===============================
#  Random Playout (baseline)
# ===============================
def random_playout(state: WordleState, wordlist):
    """Randomly play until the game ends. Return 1.0 if win else 0.0."""
    s = state.clone()
    while not s.is_terminal():
        move = random.choice(s.legal_moves(wordlist))
        s.play(move)
    return 1.0 if s.is_won() else 0.0


# ===============================
#  Entropy Playout
# ===============================
def entropy_playout(state: WordleState, wordlist):
    """
    Choose the move that maximizes information gain (entropy).
    Then play until terminal.
    """
    s = state.clone()
    while not s.is_terminal():
        moves = s.legal_moves(wordlist)
        best_move, best_entropy = None, -float("inf")

        for move in moves:
            feedback_counts = Counter()
            for w in wordlist:
                # ✅ corrige : utiliser feedback_sim
                feedback = s.feedback_sim(w, move)
                feedback_counts[feedback] += 1

            total = sum(feedback_counts.values())
            entropy = -sum((count / total) * math.log2(count / total)
                           for count in feedback_counts.values())
            if entropy > best_entropy:
                best_entropy, best_move = entropy, move

        s.play(best_move)
    return 1.0 if s.is_won() else 0.0


# ===============================
#  Frequency Playout
# ===============================
def frequency_playout(state: WordleState, wordlist):
    """
    Choose the move with the most frequent letters (in remaining candidates).
    """
    s = state.clone()
    while not s.is_terminal():
        moves = s.legal_moves(wordlist)

        # Count letter frequencies across all candidate words
        letter_counts = Counter("".join(wordlist))

        def score(word):
            return sum(letter_counts[c] for c in set(word))

        best_move = max(moves, key=score)
        s.play(best_move)

    return 1.0 if s.is_won() else 0.0


# ===============================
#  Entropy+ Playout (Entropy + Letter Diversity)
# ===============================
def entropy_plus_playout(state: WordleState, wordlist, alpha=0.7):
    """
    Hybrid playout:
    - Maximize entropy (info gain)
    - Encourage diversity of letters in guess
    alpha: weight [0,1] for entropy vs diversity
    """
    s = state.clone()
    while not s.is_terminal():
        moves = s.legal_moves(wordlist)
        best_move, best_score = None, -float("inf")

        for move in moves:
            # Compute entropy
            feedback_counts = Counter()
            for w in wordlist:
                # ✅ corrige : utiliser feedback_sim
                feedback = s.feedback_sim(w, move)
                feedback_counts[feedback] += 1

            total = sum(feedback_counts.values())
            entropy = -sum((count / total) * math.log2(count / total)
                           for count in feedback_counts.values())

            # Diversity = unique letters in the word
            diversity = len(set(move))

            score = alpha * entropy + (1 - alpha) * diversity
            if score > best_score:
                best_score, best_move = score, move

        s.play(best_move)

    return 1.0 if s.is_won() else 0.0


# ===============================
#  Frequency+ Playout (Frequency + Coverage)
# ===============================
def frequency_plus_playout(state: WordleState, wordlist, alpha=0.6):
    """
    Hybrid playout:
    - Prioritize frequent letters
    - Reward words covering as many different letters as possible
    alpha: weight [0,1] for frequency vs coverage
    """
    s = state.clone()
    while not s.is_terminal():
        moves = s.legal_moves(wordlist)

        # Letter frequency
        letter_counts = Counter("".join(wordlist))

        def score(word):
            freq_score = sum(letter_counts[c] for c in set(word))
            coverage_score = len(set(word))
            return alpha * freq_score + (1 - alpha) * coverage_score

        best_move = max(moves, key=score)
        s.play(best_move)

    return 1.0 if s.is_won() else 0.0
