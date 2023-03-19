from board_logic.board import Board
class PagodaGenerator:
    '''
        A class used to generate a pagoda function for a given equilateral triangular peg solitaire board T_n
        
        ATTRIBUTES
        board: a list of tuples (i,j) that represent cells in a board, where i is the y-axis of the board and j is the x-axis of the board
        pagoda_values:  a dictionary representing board pagoda values (key: board_cell, value: some integer in the range {-1,0,1}) 

        METHODS
        generate_pagoda_function(board):
            given a board, initiates search_values recursive method to find pagoda values for that board
            return pagoda values for the given board if they exist, or an empty set if they do not

        _search_values(to_fill_stack, filled_stack)
            recursive method for finding pagoda values 
            return True if pagoda values were found, False if they were not
    '''
    def generate_pagoda_function(self,board:Board):
        self.pagoda_values = {}
        self.board = board
        if self._search_values(self.board.skew_board.copy(),set()):
            return self.pagoda_values
        else:
            return {}
        
    def _search_values(self, to_fill_stack, filled_stack):
        # if we are at an end state and the pagoda_values are still valid, 
        if (not to_fill_stack):
            count = 0
            for peg in filled_stack:
                if (self.pagoda_values[peg] == -1):
                    count += 1
            if (count < 2):
                return False # need more -1
            return True # all constraints met, solution found
        
        current = to_fill_stack.pop()
        filled_stack.add(current) # stack of cells the function has been applied to


        # select a value
        for i in range (-1, 2):
            self.pagoda_values[current] = i 

            # check constraints...
            # check that peg(a) + peg(b) >= peg(c) for all currently valid positions
            valid = True
            for position in self.board.positions_list: # could be optimized by having a cell:position map
                c1, c2, c3 = position
                if ((c1 in filled_stack) and 
                    (c2 in filled_stack) and 
                    (c3 in filled_stack)):
                    if ((not (self.pagoda_values[c1] <= self.pagoda_values[c2] + self.pagoda_values[c3])) or 
                    (not (self.pagoda_values[c3] <= self.pagoda_values[c2] + self.pagoda_values[c1]))):
                        valid = False
                        break
                
            # check solution
            if (valid and self._search_values(to_fill_stack, filled_stack)):
                return True
            # no solution down past path, undo previous assignment
            # if current == 1:
            #     return False
        filled_stack.remove(current)
        to_fill_stack.append(current)


        return False # if we are here, we failed to find a good set of pagoda values...