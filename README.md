# Wordle-MCTS-Solver
**A Wordle solver based on Monte Carlo Tree Search (MCTS)** – Comparison of algorithm variants and playout strategies.

---
## 📂 Structure & Execution
```
WORDLE-MCTS-SOLVER/
├── results/          
├── test/                    # Unit tests       
├── main.py                    
├── experiments.py           
├── solvers.py           
├── playouts.py             
├── wordle.py           
├── utils.py                
├── wordlist.txt          
├── requirements.txt       
├── Makefile                
```

---
###  Installation & Execution
1. **Clone the repository and set up the environment:**
   ```bash
   git clone https://github.com/<user>/wordle-mcts-solver.git
   cd wordle-mcts-solver
   make setup
   ```

2. **Run experiments:**
   - **Quick mode** (debug):
     ```bash
     make quick
     ```
   - **Full experiments** (all solvers + plots):
     ```bash
     make run
     ```
   - **Generate plots only** (if CSV files exist):
     ```bash
     make plots
     ```

3. **Clean results:**
   ```bash
   make clean
   ```

4. **Run unit tests:**
   ```bash
   make test
   ```

---