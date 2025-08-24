import copy

class WordleState:
    """
    Classe représentant l'état d'une partie de Wordle.
    - secret : le mot à deviner
    - attempts : liste des (guess, feedback)
    - max_attempts : nombre maximum de coups (6 par défaut)
    """

    def __init__(self, secret, max_attempts=6):
        self.secret = secret
        self.attempts = []
        self.max_attempts = max_attempts

    def is_terminal(self):
        """Retourne True si la partie est finie (trouvé ou max tentatives)."""
        return (len(self.attempts) >= self.max_attempts
                or (self.attempts and self.attempts[-1][0] == self.secret))

    def feedback(self, guess):
        """
        Calcule le feedback (mot secret vs guess).
        Retourne une string de longueur 5 composée de :
        - 'G' (Green) : lettre correcte et bien placée
        - 'Y' (Yellow): lettre présente mais mal placée
        - 'B' (Black) : lettre absente
        """
        result = []
        for i, c in enumerate(guess):
            if c == self.secret[i]:
                result.append("G")
            elif c in self.secret:
                result.append("Y")
            else:
                result.append("B")
        return "".join(result)

    def feedback_sim(self, candidate, guess):
        """
        Simule le feedback si le mot secret était 'candidate'.
        Utile pour filtrer les mots cohérents.
        """
        result = []
        for i, c in enumerate(guess):
            if c == candidate[i]:
                result.append("G")
            elif c in candidate:
                result.append("Y")
            else:
                result.append("B")
        return "".join(result)

    def legal_moves(self, wordlist):
        """
        Retourne la liste des coups (mots) encore légaux,
        c'est-à-dire cohérents avec tous les feedbacks passés.
        """
        candidates = []
        for w in wordlist:
            ok = True
            for past_guess, past_fb in self.attempts:
                if self.feedback_sim(w, past_guess) != past_fb:
                    ok = False
                    break
            if ok:
                candidates.append(w)
        return candidates

    def play(self, guess):
        """
        Joue un mot, calcule et enregistre son feedback.
        """
        fb = self.feedback(guess)
        self.attempts.append((guess, fb))

    def score(self):
        """
        Retourne le score de la partie :
        - 1.0 si gagné (le dernier guess == secret)
        - 0.0 sinon
        """
        if self.attempts and self.attempts[-1][0] == self.secret:
            return 1.0
        return 0.0
    
    def is_won(self):
        """Retourne True si la partie est gagnée (dernier guess == secret)."""
        return self.attempts and self.attempts[-1][0] == self.secret

    def copy(self):
        """Retourne une copie profonde de l'état (utile pour les simulations)."""
        return copy.deepcopy(self)

    def clone(self):
        """Alias de copy(), pour compatibilité avec MCTS."""
        return self.copy()
