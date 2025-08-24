import os
import os
import random

def load_wordlist(path="wordlist.txt", limit=None):
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Wordlist not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        words = [w.strip().lower() for w in f if len(w.strip()) == 5]

    if not words:
        raise ValueError("Wordlist is empty or contains no 5-letter words.")

    if limit is not None:
        words = random.sample(words, min(limit, len(words)))

    return words


def save_results(stats, path="results.txt"):

    with open(path, "w", encoding="utf-8") as f:
        f.write("=== Experiment Results ===\n")
        f.write(f"Games played: {stats['n_games']}\n")
        f.write(f"Win rate: {stats['win_rate']:.2f}\n")
        f.write(f"Average guesses (wins only): {stats['avg_guesses']:.2f}\n")
        f.write(f"Distribution: {stats['distribution']}\n")
    print(f"Results saved to {path}")
