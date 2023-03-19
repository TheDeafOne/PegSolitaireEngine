from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board
from visualization.vizualizer import Visualizer
from visualization._console.consoleVisualizer import ConsoleVisualizer
import time

board = Board(4)

# board.print_state()
# print(board.skew_board)
new_board = [0] * ((board.board_size * (board.board_size+1))//2)
print(new_board)
size = board.board_size
cell_index = 0
for i in range(size-1):
    val = size-1-i
    for j in range(size-1,i-1,-1):
        new_board[val] = board.skew_board[cell_index]
        val += j
        cell_index += 1
new_board[0] = board.skew_board[-1]
print(new_board)
        


# backtrack = Backtrack(True)
# start = time.time()
# solution_stack = backtrack.backtrack(board)
# end = time.time()
# print(end-start)

# ConsoleVisualizer().visualize(solution_stack,board.board_size)
