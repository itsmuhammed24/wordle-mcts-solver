import math
import random
from collections import defaultdict
from wordle import WordleState
from playouts import random_playout 


# ===============================
#  Baseline: Random Solver
# ===============================
def random_solver(state: WordleState, wordlist):
    """Choose a random legal move."""
    moves = state.legal_moves(wordlist)
    return random.choice(moves)


# ===============================
#  Flat Monte Carlo (no tree)
# ===============================
def flat_mc(state: WordleState, wordlist, n_playouts=100, playout_fn=None):
    """
    Flat Monte Carlo Search:
    - Run many playouts for each possible move
    - Return the move with highest win rate
    """
    best_move, best_score = None, -float("inf")
    moves = state.legal_moves(wordlist)

    for move in moves:
        score_sum = 0
        for _ in range(n_playouts):
            next_state = state.clone()
            next_state.play(move)
            score_sum += playout_fn(next_state, wordlist) if playout_fn else random_playout(next_state, wordlist)

        avg_score = score_sum / n_playouts
        if avg_score > best_score:
            best_score, best_move = avg_score, move

    return best_move


# ===============================
#  UCT (Tree Search)
# ===============================
def uct_search(state: WordleState, wordlist, n_iter=100, playout_fn=None, c=1.41):
    """
    Standard UCT Search.
    Builds a tree with UCB1 selection, expansion, simulation, backpropagation.
    """
    Q = defaultdict(float)
    N = defaultdict(int)
    N_state = defaultdict(int)
    children = dict()

    def policy(state):
        if state in children:
            return max(children[state],
                       key=lambda a: Q[(state, a)] / (N[(state, a)] + 1e-9) +
                                     c * math.sqrt(math.log(N_state[state] + 1) / (N[(state, a)] + 1e-9)))
        return None

    for _ in range(n_iter):
        path, node = [], state.clone()

        # SELECTION
        while node in children and not node.is_terminal():
            a = policy(node)
            path.append((node, a))
            node = node.clone()
            node.play(a)

        # EXPANSION
        if not node.is_terminal():
            children[node] = node.legal_moves(wordlist)

        # SIMULATION
        reward = (playout_fn(node, wordlist) if playout_fn else random_playout(node, wordlist))

        # BACKPROPAGATION
        for (s, a) in path:
            N[(s, a)] += 1
            Q[(s, a)] += reward
            N_state[s] += 1

    legal = state.legal_moves(wordlist)
    return max(legal, key=lambda a: Q[(state, a)] / (N[(state, a)] + 1e-9))


# ===============================
#  UCT + RAVE
# ===============================
def uct_rave_search(state: WordleState, wordlist, n_iter=100, playout_fn=None, c=1.41):
    """
    UCT with RAVE (Rapid Action Value Estimation).
    Uses statistics of actions seen in simulations (not only direct descendants).
    """
    Q, N, N_state, children = defaultdict(float), defaultdict(int), defaultdict(int), dict()
    Q_rave, N_rave = defaultdict(float), defaultdict(int)

    def beta(n):
        k = 300
        return k / (n + k)

    def policy(state):
        if state in children:
            def ucb1_rave(a):
                q = Q[(state, a)] / (N[(state, a)] + 1e-9)
                q_rave = Q_rave[(state, a)] / (N_rave[(state, a)] + 1e-9)
                b = beta(N[(state, a)])
                combined_q = (1 - b) * q + b * q_rave
                exploration = c * math.sqrt(math.log(N_state[state] + 1) / (N[(state, a)] + 1e-9))
                return combined_q + exploration
            return max(children[state], key=ucb1_rave)
        return None

    for _ in range(n_iter):
        path, node = [], state.clone()
        actions_played = []

        # SELECTION
        while node in children and not node.is_terminal():
            a = policy(node)
            path.append((node, a))
            actions_played.append(a)
            node = node.clone()
            node.play(a)

        # EXPANSION
        if not node.is_terminal():
            children[node] = node.legal_moves(wordlist)

        # SIMULATION
        reward = (playout_fn(node, wordlist) if playout_fn else random_playout(node, wordlist))

        # BACKPROPAGATION
        for (s, a) in path:
            N[(s, a)] += 1
            Q[(s, a)] += reward
            N_state[s] += 1
            for rave_a in actions_played:
                N_rave[(s, rave_a)] += 1
                Q_rave[(s, rave_a)] += reward

    legal = state.legal_moves(wordlist)
    return max(legal, key=lambda a: Q[(state, a)] / (N[(state, a)] + 1e-9))


# ===============================
#  UCT + GRAVE
# ===============================
def uct_grave_search(state: WordleState, wordlist, n_iter=100, playout_fn=None, c=1.41):
    """
    UCT with GRAVE (Generalized RAVE).
    Reduces RAVE bias when moves are not symmetric.
    """
    Q, N, N_state, children = defaultdict(float), defaultdict(int), defaultdict(int), dict()
    Q_rave, N_rave = defaultdict(float), defaultdict(int)

    def beta(n, n_rave):
        return n_rave / (n + n_rave + 1e-9)

    def policy(state):
        if state in children:
            def ucb1_grave(a):
                q = Q[(state, a)] / (N[(state, a)] + 1e-9)
                q_rave = Q_rave[(state, a)] / (N_rave[(state, a)] + 1e-9)
                b = beta(N[(state, a)], N_rave[(state, a)])
                combined_q = (1 - b) * q + b * q_rave
                exploration = c * math.sqrt(math.log(N_state[state] + 1) / (N[(state, a)] + 1e-9))
                return combined_q + exploration
            return max(children[state], key=ucb1_grave)
        return None

    for _ in range(n_iter):
        path, node = [], state.clone()
        actions_played = []

        # SELECTION
        while node in children and not node.is_terminal():
            a = policy(node)
            path.append((node, a))
            actions_played.append(a)
            node = node.clone()
            node.play(a)

        # EXPANSION
        if not node.is_terminal():
            children[node] = node.legal_moves(wordlist)

        # SIMULATION
        reward = (playout_fn(node, wordlist) if playout_fn else random_playout(node, wordlist))

        # BACKPROPAGATION
        for (s, a) in path:
            N[(s, a)] += 1
            Q[(s, a)] += reward
            N_state[s] += 1
            for rave_a in actions_played:
                N_rave[(s, rave_a)] += 1
                Q_rave[(s, rave_a)] += reward

    legal = state.legal_moves(wordlist)
    return max(legal, key=lambda a: Q[(state, a)] / (N[(state, a)] + 1e-9))


# ===============================
#  Nested Monte Carlo Search
# ===============================
def nested_mc_search(state: WordleState, wordlist, level=1, playout_fn=None):
    """
    Nested Monte Carlo Search (NMCS).
    - Level 0: random playout
    - Level n: recursive search, keep best sequence found
    """
    if level == 0:
        return random.choice(state.legal_moves(wordlist))

    best_move, best_score = None, -float("inf")

    for move in state.legal_moves(wordlist):
        next_state = state.clone()
        next_state.play(move)

        # Recursive call
        if next_state.is_terminal():
            score = 1.0 if next_state.is_won() else 0.0
        else:
            nested_move = nested_mc_search(next_state, wordlist, level - 1, playout_fn)
            next_state.play(nested_move)
            score = (playout_fn(next_state, wordlist) if playout_fn else random_playout(next_state, wordlist))

        if score > best_score:
            best_score, best_move = score, move

    return best_move
