from board_logic.board import Board
class PagodaGenerator:
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