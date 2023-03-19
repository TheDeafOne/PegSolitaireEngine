from visualization.vizualizer import Visualizer
from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board
import time

print("An Algorithm to Solve Triangular Peg Solitaire using Enhanced Backtracking Methods")
size_desired = input("Enter Desired Board Size to Test:")

board = Board(10)
backtrack = Backtrack(True)
s = time.time()
backtrack.backtrack(board)
e = time.time()
print(f"The length of the Backtrack Solution Stack: {len(backtrack.solution_stack)}")
print(f"The time in seconds to find a solution for board size {size_desired}: {e-s}")