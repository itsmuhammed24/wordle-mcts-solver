import pytest
from wordle import WordleState
from solvers import random_solver, flat_mc, uct_search
from playouts import random_playout, entropy_playout, frequency_playout

# Petit dictionnaire de test
WORDLIST = ["crane", "trace", "stone", "spill", "party"]

def test_random_solver_returns_valid_move():
    state = WordleState("crane")
    move = random_solver(state, WORDLIST)
    assert move in WORDLIST

def test_flat_mc_with_random_playout():
    state = WordleState("crane")
    move = flat_mc(state, WORDLIST, n_playouts=10, playout_fn=random_playout)
    assert move in WORDLIST

def test_flat_mc_with_entropy_playout():
    state = WordleState("crane")
    move = flat_mc(state, WORDLIST, n_playouts=10, playout_fn=entropy_playout)
    assert move in WORDLIST

def test_uct_search_with_random_playout():
    state = WordleState("crane")
    move = uct_search(state, WORDLIST, n_iter=20, playout_fn=random_playout)
    assert move in WORDLIST

def test_uct_search_with_frequency_playout():
    state = WordleState("crane")
    move = uct_search(state, WORDLIST, n_iter=20, playout_fn=frequency_playout)
    assert move in WORDLIST
