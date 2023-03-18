from visualization.vizualizer import Visualizer
from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board
import time

for i in range (9, 12):

    #time_vals = []
    board = Board(i)
    backtrack = Backtrack()
    first = time.time()
    backtrack.backtrack(board)
    final = time.time()

    tdelta = final - first
    print(tdelta)
    #time_vals.append(tdelta)

    print(f"Time value for board size {i}: {tdelta}")
    #average = sum(time_vals)/len(time_vals)
    #print(f"Average for board size {i}: {average}")

def print_state(state, board_size):
    predent = " " * board_size
    st = predent[1:]
    fwtick = 1
    cnt = 0
    for i in range(board_size):
        for j in range(i+1):
            value = (j,i)
            if cnt == fwtick:
                fwtick += 1
                cnt = 0
                st += "\n" + predent[fwtick:]
            st += str(state[value]) + " "
            cnt += 1

    
    print(st)


for state in backtrack.solution_stack:
     print_state(state,board.board_size)
