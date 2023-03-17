from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board
from visualization.vizualizer import Visualizer
import time

board = Board(6)
backtrack = Backtrack()
start = time.time()
backtrack.backtrack(board)
end = time.time()
print(end-start)
