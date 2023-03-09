from board_logic.board import Board

class Backtrack:
    '''
        A class used to solve a given peg solitaire board with backtracking

        ATTRIBUTES
        solution_stack: a stack of states that track the moves made, where only the moves that lead to the solution are kept

        METHODS
        backtrack(board)
            solves the given board using backtracking 
            returns True if board can be solved, False otherwise
    '''
    def __init__(self):
        self.solution_stack = []


    '''
        Uses backtracking to solve the given board

        PARAMS
        board: a class representing the current peg solitaire board

        RETURNS 
        True if board can be solved, False otherwise 
    '''
    def backtrack(self, board: Board) -> bool:
        # check if board has been solved
        if board.board_state == board.goal_state:
            return True
        
        # get list of possible positions and current state
        positions_list = board.positions_list
        board_state = board.board_state

        # cycle through positions, taking a jump at any viable position
        # a viable position is any position that has the form (1, 1, 0) or (0, 1, 1) 
        for position in positions_list:
            # check if position is jumpable
            if ((board_state[position[0]] and board_state[position[1]] and not board_state[position[2]]) or 
                (not board_state[position[0]] and board_state[position[1]]and board_state[position[2]])):
                board.jump(position)
                self.solution_stack.append(board.board_state.copy())
                solution = self.backtrack(board)

                # a solution was found, push up the tree
                if solution:
                    return True
                
                # undo previous jump
                board.jump(position) 
                # jump was not part of solution state, so it must be removed from the solution stack
                self.solution_stack.pop()

        # no solution could be found
        return False