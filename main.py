from utils import load_wordlist
from experiments import (
    run_comparisons,
    plot_winrates,
    plot_avg_guesses,
    plot_histogram,
    plot_cdf
)
import pandas as pd 

if __name__ == "__main__":
 
    words = load_wordlist("wordlist.txt", limit=1000)

    print("\n⚡ Running main experiments...")
    df = run_comparisons(words, n_games=50, save_path="results.csv")

  
    df_dist = pd.read_csv("distribution.csv")


    plot_winrates(df, save_path="plot_winrate.png")
    plot_avg_guesses(df, save_path="plot_avg_guesses.png")

    solvers_to_compare = ["RandomSolver", "FlatMC (entropy)", "UCT+RAVE", "UCT+GRAVE"]
    plot_histogram(df_dist, solvers_to_compare, save_path="plot_histogram.png")
    plot_cdf(df_dist, solvers_to_compare, save_path="plot_cdf.png")

    print("\n Figures générées : plot_winrate.png, plot_avg_guesses.png, plot_histogram.png, plot_cdf.png")
