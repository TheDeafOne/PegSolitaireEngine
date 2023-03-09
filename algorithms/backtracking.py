from board_logic.board import Board
class Backtrack:
    def __init__(self):
        pass
    

    def backtrack(self, board: Board,count=0) -> bool:
        if board.board_state == board.goal_state:
            print(count-1)
            return True
        positions_list = board.positions_list
        board_state = board.board_state
        for position in positions_list:
            # check if position is jumpable
            if ((board_state[position[0]] and board_state[position[1]] and not board_state[position[2]]) or 
                (not board_state[position[0]] and board_state[position[1]]and board_state[position[2]])):
                # print([board.board_state[x] for x in position])
                board.jump(position)
                board.stack.append(board.board_state.copy())
                # print((a,b))
                solution = self.backtrack(board,count+1)
                if solution:
                    return True
                board.jump(position) # undo previous jump
                board.stack.pop()
                # board.stack.pop()

        return False

