import random
import time
from BaseAI import BaseAI

class IntelligentAgent(BaseAI):
    def __init__(self):
        self.start_time = None
        self.time_limit = 0.18
        self.max_depth = 6

    def getMove(self, grid):
        ''' Returns the best move using iterative deepening with expectiminimax until timeout '''
        self.start_time = time.time()
        move = None
        depth = 1

        try:
            while True:
                self.max_depth = depth
                move = self.expectiminimax(grid, 0)
                depth += 1
        except TimeoutError:
            pass
    
        return move if move is not None else random.choice(grid.getAvailableMoves())[0]

    def timeTest(self, grid, depth):
        ''' Returns True if the time limit or max depth has been reached; 
            raises TimeoutError if timeout exceeded '''
        if time.time() - self.start_time > self.time_limit:
            raise TimeoutError()
        if depth == self.max_depth or not grid.getAvailableMoves():
            return True
        return False

    def expectiminimax(self, grid, depth):
        ''' Begins the expectiminimax search and returns the best move at the root '''
        alpha, beta = float('-inf'), float('inf')
        move = self.maxNode(grid, depth, alpha, beta)
        return move[0]

    def maxNode(self, grid, depth, alpha, beta):
        ''' Maximizing player in expectiminimax; 
            uses alpha-beta pruning to return best move and value '''
        if self.timeTest(grid, depth):
            return None, self.heuristics(grid)

        max_value = float('-inf')
        best_move = None
        avail_moves = grid.getAvailableMoves()
        
        for move in avail_moves:
            _, value = self.chanceNode(move[1], depth + 1, alpha, beta)
            if value > max_value:
                max_value = value
                best_move = move[0]
            alpha = max(alpha, value)
            if beta <= alpha:
                break  #beta cut-off

        return best_move, max_value

    def chanceNode(self, grid, depth, alpha, beta):
        ''' Chance node simulating expected value from 2 or 4 tile spawns '''
        if self.timeTest(grid, depth):
            return None, self.heuristics(grid)

        prob_two = self.minNode(grid, depth + 1, alpha, beta, 2) * 0.9
        prob_four = self.minNode(grid, depth + 1, alpha, beta, 4) * 0.1
        expected_value = prob_two + prob_four

        return None, expected_value

    def minNode(self, grid, depth, alpha, beta, num):
        ''' Minimizing player simulating adversarial tile placement; 
            returns lowest heuristic value across placements '''
        if self.timeTest(grid, depth):
            return self.heuristics(grid)

        min_value = float('inf')
        available_cells = grid.getAvailableCells()

        for cell in available_cells:
            grid_clone = grid.clone()
            grid_clone.insertTile(cell, num)
            _, value = self.maxNode(grid_clone, depth + 1, alpha, beta)
            if value < min_value:
                min_value = value
            beta = min(beta, value)
            if beta <= alpha:
                break  #alpha cut-off

        return min_value

    def heuristics(self, grid):
        ''' Combines multiple features (empty cells, merges, monotonicity, corner strategy) 
            into a single evaluation score '''
        empty_cells = len(grid.getAvailableCells())
        num_merges = self.numMerges(grid, empty_cells)
        mono_score = self.monotonicity(grid)
        corner_score = self.cornerScore(grid)
        return empty_cells + 0.5*num_merges + 0.2*mono_score + corner_score
    
    def numMerges(self, grid, cells):
        ''' Approximates the number of tile merges from available player moves '''
        merges = 0
        for move in grid.getAvailableMoves():
            new_grid = move[1]
            new_cells = new_grid.getAvailableCells()
            merges += cells - len(new_cells)
        return merges
    
    def monotonicity(self, grid):
        ''' Measures how smoothly values increase or decrease across rows and columns, 
            favoring ordered gradients '''
        mono_score = 0

        for x in range(grid.size):
            curr_row = grid.map[x]
            for i in range(len(curr_row) - 1):
                if curr_row[i] is not None and curr_row[i + 1] is not None:
                    if curr_row[i] <= curr_row[i + 1]:
                        mono_score += curr_row[i]
                    else:
                        mono_score -= curr_row[i]
        for y in range(grid.size):
            for x in range(grid.size - 1):
                if grid.map[x][y] is not None and grid.map[x + 1][y] is not None:
                    if grid.map[x][y] <= grid.map[x + 1][y]:
                        mono_score += grid.map[x][y]
                    else:
                        mono_score -= grid.map[x][y]

        return mono_score
    
    def cornerScore(self, grid):
        ''' Encourages highest tile in bottom-right and rewards proximity of large values to that corner '''
        corner_score = 0
        bottom_right = (grid.size - 1, grid.size - 1)
        max_tile = grid.getMaxTile()

        if grid.map[bottom_right[0]][bottom_right[1]] == max_tile:
            corner_score += max_tile

        for x in range(grid.size):
            for y in range(grid.size):
                if grid.map[x][y] is not None:
                    distance = abs(bottom_right[0] - x) + abs(bottom_right[1] - y)
                    corner_score += grid.map[x][y] / (distance + 1)

        return corner_score
