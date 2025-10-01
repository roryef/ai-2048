Rory Eastland-Fruit
November 2024
AI-Powered 2048 Game Solver

Overview
--------
This project implements an adversarial search agent that plays the 2048 puzzle using the expectiminimax algorithm with alpha beta pruning. 
The game is modeled as a two player interaction between a Player AI that issues board moves and a Computer AI that spawns new tiles with probabilities 
0.9 for 2 and 0.1 for 4. The agent uses iterative deepening to respect a strict per-move time budget and falls back safely if time is exhausted.

How to run
----------
1. Ensure Python 3 is installed.
2. From the project directory run: python3 GameManager.py
   The driver initializes the grid with two random tiles, alternates player and computer turns, prints the board after each turn, and terminates the game 
   when no moves remain or the time budget is exceeded. The program prints the maximum tile achieved.

Key features
------------
* Expectiminimax search with max, chance, and min nodes that reflect player decisions, stochastic spawns, and adversarial tile placement respectively, 
    combined with alpha beta pruning for efficiency.
* Iterative deepening loop that increases depth until a time test fires, ensuring decisions are returned within the 0.2 second move limit plus allowance 
    defined by the driver.
* Heuristic evaluation that combines open cell count, merge potential estimated from successor states, board monotonicity, and a corner strategy that 
    prefers concentrating large tiles in the bottom right.

Repository structure
--------------------
* GameManager.py controls the game loop, enforces the move time limit, alternates turns, and returns the final maximum tile. Run this file to play or 
    evaluate the agent.
* Grid.py implements the 4x4 board, legal moves, tile merging, and helpers such as clone, getAvailableMoves, and getAvailableCells that the agent queries 
    during search.
* BaseAI.py is the simple interface all AIs implement.
* ComputerAI.py chooses a random empty cell for tile insertion during the computer’s turn.
* Displayer.py renders the grid in the terminal using ANSI colors or a Windows fallback.
* IntelligentAgent.py contains the expectiminimax player with pruning, iterative deepening, time checks, and heuristics.
* TestDisplay.py provides a small harness to preview the board renderer with a mock grid.

Algorithm design
----------------
Search formulation:
The root call evaluates player actions at max nodes. Each successor transitions to a chance node that computes the expected value of the next board by 
combining min nodes that simulate adversarial placements of 2 and 4 weighted by 0.9 and 0.1. Min nodes insert a tile into each available cell and select 
the worst continuation by recursing to a max node. Pruning uses standard alpha and beta bounds at max and min layers.

Time management:
The agent performs iterative deepening: it sets a depth target, searches to that depth, records the best move, then increases depth and repeats until a 
timeout is raised by a shared time test. GameManager enforces approximately 0.2 seconds per move with a small allowance, so the agent uses a slightly 
lower internal limit and always returns the last known best move on timeout.

Heuristic evaluation:
The evaluation function is applied at cutoffs determined by depth and time. These signals are combined linearly, and the relative weights can be tuned by 
experiment. It blends:

* Empty cells to preserve mobility
* Merge potential, approximated by the change in open cells across immediate legal player moves
* Monotonicity to encourage smooth gradients in rows and columns
* Corner preference to keep the largest tile anchored in the bottom right and to reward proximity of large tiles to that corner

Design choices and tradeoffs
----------------------------
* Expectiminimax was chosen to model the stochastic opponent and to reason over adversarial tile placements while respecting the spawn probabilities. 
    This approach captures both randomness and worst-case branching in a single framework.
* Alpha beta pruning and move ordering reduce node expansions and make deeper searches feasible within the time budget.
* Iterative deepening provides a good early answer that improves with time and ensures the agent always meets the per-move deadline.
* Heuristics were selected to reflect widely used 2048 strategies, including keeping a stable gradient toward a corner, preserving mobility, and 
    prioritizing merges. The merge approximation leverages the grid’s available-successor interface for efficiency.

Extensibility
-------------
The agent can be extended with additional features such as smoother move ordering guided by heuristic pre-scores, adaptive weights learned from self-play logs, 
or alternative corner preferences by rotating the board or swapping the corner target in the corner heuristic. The module boundaries in the skeleton make it 
straightforward to test new ideas without changing the driver or grid mechanics.
