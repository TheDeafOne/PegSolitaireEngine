from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board
from visualization.vizualizer import Visualizer
from visualization._console.consoleVisualizer import ConsoleVisualizer
import time

board = Board(4)
board.print_state()
print(board.skew_board)




# backtrack = Backtrack(True)
# start = time.time()
# solution_stack = backtrack.backtrack(board)
# end = time.time()
# print(end-start)

# ConsoleVisualizer().visualize(solution_stack,board.board_size)
