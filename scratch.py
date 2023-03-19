from visualization.vizualizer import Visualizer
from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board
import time

board = Board(8)
backtrack = Backtrack(True)
s = time.time()
backtrack.backtrack(board)
e = time.time()
print(len(backtrack.solution_stack))
print(e-s)
