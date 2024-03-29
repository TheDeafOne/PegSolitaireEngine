from board_logic.board import Board
from ..pagoda.pagoda import PagodaGenerator
import time

class Backtrack:
    '''
        A class used to solve a given peg solitaire board with backtracking

        ATTRIBUTES
        solution_stack: a stack of states that track the moves made, where only the moves that lead to the solution are kept
        termination_states: a set of string representations of previously encoutnered unsolvable board states
        use_pagoda: boolean flag for whether backtrack will use a pagoda function
        pagoda_generator: a class for generating a pagoda function for a given board
        pagoda_function: dictionary representing the given board's pagoda values (key: board cell, value: integer in range {-1,0,1})
        
        METHODS
        backtrack(board)
            solves the given board using backtracking 
            returns True if board can be solved, False otherwise
    '''

    def __init__(self, use_pagoda=False,is_game_loop=False):
        self.solution_stack = []
        self.termination_states = set()
        self.use_pagoda = use_pagoda
        self.is_game_loop = is_game_loop
        self.next_step = False
        self.did_solve = False
        self.pagoda_generator = PagodaGenerator()
        self.pagoda_function = {}

    '''
        starts backtracking with different specified algorithms

        PARAMS
        board: a class representing the current peg solitaire board

        RETURNS 
        The solution stack if board can be solved, False otherwise 
    '''
    def backtrack(self, board: Board) -> bool:
        self.solution_stack = []

        # add pagoda function if requested
        if self.use_pagoda:
            self.pagoda_function = self.pagoda_generator.generate_pagoda_function(board)
            if not self.pagoda_function:
                # no pagoda function for given board
                self.use_pagoda = False

        # begin backtracking
        # manage gameloop sleep for polling
                if self.is_game_loop:
                    self.next_step = False
                    while not self.next_step:
                        time.sleep(0.01)
        if self._search(board):
            self.did_solve = True
            return self.solution_stack
        
        # no solution for board
        return False

    '''
        uses backtracking to solve the given board

        PARAMS
        board: a class representing the current peg solitaire board

        RETURNS 
        The solution stack if board can be solved, False otherwise 
    '''
    def _search(self, board: Board):
        # get list of possible positions and current state
        positions_list = board.positions_list
        board_state = board.board_state

        # check if board has been solved
        if board.board_state == board.goal_state:
            return True

        # check if board state, its rotation, or its reflection is memoized
        if (board.get_board_string() in self.termination_states
            or ''.join(map(str,[board.board_state[x] for x in board.rotation()])) in self.termination_states
            or ''.join(map(str,[board.board_state[x] for x in board.mirror()])) in self.termination_states):
            return False

        if self.use_pagoda:
            pagoda_count = 0
            for cell in board_state:
                if board_state[cell]:
                    pagoda_count += self.pagoda_function[cell]
            if pagoda_count <= self.pagoda_function[(0, 0)]:
                self.termination_states.add(board.get_board_string())
                return False

        # cycle through positions, taking a jump at any viable position
        # a viable position is any position that has the form (1, 1, 0) or (0, 1, 1)
        for position in positions_list:
            # check if position is jumpable
            if ((board_state[position[0]] and board_state[position[1]] and not board_state[position[2]]) or
                    (not board_state[position[0]] and board_state[position[1]] and board_state[position[2]])):
                board.jump(position)
                self.solution_stack.append(board.board_state.copy())
                solution = self._search(board)

                # a solution was found, push up the tree
                if solution:
                    return True

                # undo previous jump
                board.jump(position)
                # jump was not part of solution state, so it must be removed from the solution stack
                self.solution_stack.pop()

        # no solution could be found
        self.termination_states.add(board.get_board_string())
        return False
