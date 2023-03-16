from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board

board = Board(5)
# backtrack = Backtrack()
# backtrack.backtrack(board)


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


# for state in backtrack.solution_stack:
#     print_state(state,board.board_size)