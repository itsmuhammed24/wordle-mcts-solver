import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from wordle import WordleState
from playouts import (
    random_playout,
    entropy_playout,
    frequency_playout,
    entropy_plus_playout,
    frequency_plus_playout,
)
from solvers import (
    random_solver,
    flat_mc,
    uct_search,
    uct_rave_search,
    uct_grave_search,
    nested_mc_search,
)


SOLVER_COLORS = {
    "RandomSolver": "tab:blue",
    "FlatMC (random)": "tab:green",
    "FlatMC (entropy)": "tab:orange",
    "UCT (random)": "tab:red",
    "UCT (freq+)": "tab:purple",
    "UCT+RAVE": "tab:cyan",
    "UCT+GRAVE": "tab:brown",
    "NMCS (level 1)": "tab:pink",
    "NMCS (level 2)": "tab:olive",
}


# ===============================
#  Core evaluation
# ===============================
def play_game(secret, solver, wordlist, max_attempts=6):
    """Play a full Wordle game with the given solver."""
    state = WordleState(secret, max_attempts=max_attempts)
    while not state.is_terminal():
        move = solver(state, wordlist)
        if move is None: 
            break
        state.play(move)
    return state


def evaluate(solver, wordlist, n_games=50, verbose=False):
    """Evaluate a solver across multiple games."""
    results = []
    secrets = random.sample(wordlist, min(n_games, len(wordlist)))

    for secret in secrets:
        state = play_game(secret, solver, wordlist)
        if verbose:
            print(f"Secret: {secret}, Attempts: {len(state.attempts)}, Win: {state.score()}")
        results.append(len(state.attempts) if state.score() == 1 else 0)

    successes = sum(1 for r in results if r > 0)
    win_rate = successes / len(results)
    avg_guesses = np.mean([r for r in results if r > 0]) if successes > 0 else 0

    stats = {
        "n_games": len(results),
        "win_rate": win_rate,
        "avg_guesses": avg_guesses,
        "distribution": results,
    }

    return stats


# ===============================
#  Plots
# ===============================

def plot_winrates(df, save_path=None):
    """Bar plot des win rates par solver (fond blanc style publication)."""
    plt.figure(figsize=(10, 5), facecolor="white")
    bars = plt.bar(df["Solver"], df["WinRate"], color="skyblue", edgecolor="black")
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Win Rate")
    plt.title("Win Rate per Solver", fontsize=14)
    for bar, val in zip(bars, df["WinRate"]):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{val:.2f}",
                 ha="center", va="bottom", fontsize=9)
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()


def plot_avg_guesses(df, save_path=None):
    """Bar plot du nombre moyen de guesses par solver."""
    plt.figure(figsize=(10, 5), facecolor="white")
    bars = plt.bar(df["Solver"], df["AvgGuesses"], color="lightgreen", edgecolor="black")
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Average Guesses (Wins Only)")
    plt.title("Average Guesses per Solver", fontsize=14)
    for bar, val in zip(bars, df["AvgGuesses"]):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{val:.2f}",
                 ha="center", va="bottom", fontsize=9)
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()


def plot_histogram(df_dist, solvers_to_compare, save_path=None):
    """Histogramme comparatif (distribution des guesses pour quelques solveurs)."""
    plt.figure(figsize=(10, 5), facecolor="white")
    for solver in solvers_to_compare:
        subset = df_dist[(df_dist["Solver"] == solver) & (df_dist["Guesses"] != "fail")].copy()
        subset["Guesses"] = subset["Guesses"].astype(int)
        plt.bar(subset["Guesses"], subset["Count"], alpha=0.6, label=solver)
    plt.xlabel("Number of guesses")
    plt.ylabel("Frequency")
    plt.title("Guess Distribution", fontsize=14)
    plt.legend(frameon=False)
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()


def plot_cdf(df_dist, solvers_to_compare, save_path=None):
    """CDF comparative (probabilité cumulée de réussite)."""
    plt.figure(figsize=(10, 5), facecolor="white")
    for solver in solvers_to_compare:
        subset = df_dist[(df_dist["Solver"] == solver) & (df_dist["Guesses"] != "fail")].copy()
        subset["Guesses"] = subset["Guesses"].astype(int)
        expanded = np.repeat(subset["Guesses"].values, subset["Count"].values)
        expanded = np.sort(expanded)
        cdf = np.arange(1, len(expanded)+1) / len(expanded)
        plt.step(expanded, cdf, where="post", label=solver)
    plt.xlabel("Number of guesses")
    plt.ylabel("Cumulative Success Probability")
    plt.title("CDF of Success", fontsize=14)
    plt.legend(frameon=False)
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.show()



def run_comparisons(wordlist, n_games=50, save_path=None):
    """
    Run experiments on all solvers + playouts.
    Returns a pandas DataFrame with results.
    """


    solvers = {
    "RandomSolver": lambda s, wl: random_solver(s, wl),
    "FlatMC (entropy)": lambda s, wl: flat_mc(s, wl, n_playouts=50, playout_fn=entropy_playout),
    "UCT": lambda s, wl: uct_search(s, wl, n_iter=100, playout_fn=random_playout),
    "UCT+GRAVE": lambda s, wl: uct_grave_search(s, wl, n_iter=100, playout_fn=frequency_plus_playout),
}


    



    records = []
    for name, solver in solvers.items():
        print(f"=== Evaluating {name} ===")
        stats = evaluate(solver, wordlist, n_games=n_games)
        records.append({
            "Solver": name,
            "WinRate": stats["win_rate"],
            "AvgGuesses": stats["avg_guesses"],
        })

    df = pd.DataFrame(records)

    if save_path:
        df.to_csv(save_path, index=False)
        print(f"\n Results saved to {save_path}")

    print("\n=== Comparative Results ===")
    print(df.to_string(index=False))

    return df
