class Board():
    '''
        A class used to manage and represent a peg solitaire board
        A board can be referenced to as T, where a board is an equilateral triangle. A board with sides of length n is T_n
        
        ATTRIBUTES
        board_size: and integer representing the length of one side of the board (n in T_n)
        _alphabetic_values: a string of all the index values for a given board, where a board T_n uses n chars from this string as an x-index
        skew_board: a list of tuples (i,j) that represent cells in a board, where i is the y-axis of the board and j is the x-axis of the board
        alphanumeric_board: a list of tuples (l,j) that represent cells in a board, where l is a char from _alphabetic_values that represents the x-axis and j is a int representing the y-axis
        board_map: a dictionary representing the board index values (key: skew_board_value, value: alphanumeric_board_value)
        board_state: a dictionary reprenting the current boards state (key: skew_board_value, value: peg_value), 
            where peg_value is 1 if a peg is in that postion, and 0 otherwise
        _generate_pagoda_values: a dictionary representing the board's pagoda ... (key: skew_board_value, value: pagoda_value),
            where pagoda_value is in the range {-1, 0, 1}
        goal_state: a dictionary representing the goal state that is trying to be reached (key: skew_board_value, value: peg_value)
        _hash_skew_board: a set represention of the skew_board list
        positions_list: a list of positions p, represented by the tuple <(c_i-1,c_i,c_i+1)> of positions that the board has, 
            where c is a given cell in the board, and every c in any p is in the in the board
        
        METHODS
        _validate_positions(position): 
            checks that for every cell c in a given position, no c is outside the set board, identified by hash_skew_board
            returns true if position is valid, false otherwise
        
        _map_positions():
            finds all possible positions for the given board size, and sets the positions list according to the validated positions
            returns list
        
        jump(position):
            given a position (a,b,c), take a jump action where a jump action one of the two:
                1. a = 1, b = 1, c = 0 -> a = 0, b = 0, c = 1
                2. a = 0, b = 1, c = 1 -> a = 1, b = 0, c = 0
            return None

        _generate_pagoda():
            ...
            return bool

        _verify_pagoda():
            ...
            return bool                
        
        
    '''
    def __init__(self,board_size=4, initial_state_positions=[(0,0)], goal_state_positions=[(0,0)]):
        self.board_size = board_size

        # set up board maps and everything necessary for identifying individual cells on a board
        self._alphabetic_values = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.skew_board = [(i,j) for i in range(self.board_size) for j in range(i,self.board_size)]
        self.alphanumeric_board = [self._alphabetic_values[pair[0]] + str(pair[1]+1) for pair in self.skew_board]
        self.board_map = dict(zip(self.skew_board,self.alphanumeric_board))

        # get possible positions for given board size
        self._hash_skew_board = set(self.skew_board)
        self.positions_list = self._map_positions()

        # set current state and goal state of board
        self.board_state = dict(zip(self.skew_board,[1] * len(self.skew_board)))
        self.goal_state = dict(zip(self.skew_board,[0] * len(self.skew_board)))
        self.pagoda_values = dict(zip(self.skew_board, [0] * len(self.skew_board)))
        if (not self._generate_pagoda_values()):
            print('Failed to find pagoda values')
        else:
            print('Successfully found pagoda values:')
            self._pagoda_print_state()
        for position in initial_state_positions:
            self.board_state[position] = 0
        for position in goal_state_positions:
            self.goal_state[position] = 1


    '''
        Validates a given position p, ensuring that no cell c in p is outside the defined board using the hash_skew_map

        PARAMS
        position: a tuple of three cells (a, b, c)

        RETURNS
        True if the position is valid, False otherwise
    '''
    def _validate_position(self, position):
        return position[0] in self._hash_skew_board and position[1] in self._hash_skew_board and position[2] in self._hash_skew_board


    '''
        Finds all the possible positions for the given board size, and sets the positions list according to the valid positions

        RETURNS
        list of valid positions
    '''
    def _map_positions(self):
        positions_list = []
        for i in range(0,self.board_size):
            for j in range(i,self.board_size):
                # locate all possible positions relative to a center cell at (i,j)
                horizontal_position = [(i-1,j),(i,j),(i+1,j)]
                left_diagonal_position = [(i,j-1),(i,j),(i,j+1)]
                right_diagonal_position = [(i-1,j-1),(i,j),(i+1,j+1)]

                # validate each found position to ensure that only valid positions are added
                # a valid position is one with no cells 
                if self._validate_position(horizontal_position):
                    positions_list.append(horizontal_position)
                if self._validate_position(left_diagonal_position):
                    positions_list.append(left_diagonal_position)                    
                if self._validate_position(right_diagonal_position):
                    positions_list.append(right_diagonal_position)
        return positions_list

    '''
        Takes a jump action on the given position
                
        PARAMS
        a position represented by a tuple of cells (a, b, c)

        RETURNS
        None
    '''
    def jump(self,position):
        self.board_state[position[0]] ^= 1
        self.board_state[position[1]] ^= 1
        self.board_state[position[2]] ^= 1    

    '''
        Generates a set of pagoda values 

        RETURNS
        True if solution found, false otherwise
    '''    
    def _generate_pagoda_values(self):
        filled_stack = []
        to_fill_stack = []
        for i in range(0,self.board_size):
            for j in range(0,i+1):
                to_add = (j,i)
                to_fill_stack.append(to_add)
                print(str(to_add))
        
        # print('current stack:')
        # for peg in to_fill_stack:
        #     print(str(peg))

        for position in self.positions_list:
            print(str(position[0]) + ' ' + str(position[1]) + ' ' + str(position[2]))

        return self._pagoda_values_backtrack(to_fill_stack.copy(),filled_stack.copy())


    '''
        Recursive helper backtracking method for finding a set of pagoda values 

        RETURNS
        True if solution found, false otherwise
    '''  
    def _pagoda_values_backtrack(self, to_fill_stack, filled_stack):
        valid = False # holds whether the current pagoda_values are valid
        solution_found = False
        current = to_fill_stack.pop()
        print('current is ' + str(current))
        filled_stack.append(current)

        # print('current filled stack:')
        # for peg in filled_stack:
        #     print(str(peg))

        # select a value
        for i in range (-1, 2):
            print(str(current) + ' filled with ' + str(i))
            self.pagoda_values[current] = i 
            valid = True

            self._pagoda_print_state()

            # check constraints...
            # check that peg(a) + peg(b) >= peg(c) for all currently valid positions
            for position in self.positions_list:
                if (position[0] in filled_stack and position[1] in filled_stack and position[2] in filled_stack):
                    #print('found tuple with pegs ' + str(position[0]) + ' ' + str(position[1]) + ' ' + str(position[2]) + ' ')
                    if (not ((self.pagoda_values[position[0]] + self.pagoda_values[position[1]] >= self.pagoda_values[position[2]]) and 
                        (self.pagoda_values[position[2]] + self.pagoda_values[position[1]] >= self.pagoda_values[position[0]]))):
                        valid = False
                        # print('invalid tuple')
                
            # if we are at an end state and the pagoda_values are still valid, 
            #   check that there are at least two -1 occurances
            if (not to_fill_stack and valid):
                count = 0
                for peg in filled_stack:
                    if (self.pagoda_values[peg] == -1):
                        count += 1
                if (count < 2):
                    valid = False
                    #self.pagoda_print_state()
                    print(str(count) + ' so invalid solution')
                else:
                    return True # we have found a solution!
                
            # if we have made a good move, recursive call
            if (valid):
                solution_found = self._pagoda_values_backtrack(to_fill_stack.copy(), filled_stack.copy())              
                if (solution_found):
                    return True

        self.pagoda_values[current] = 0
        #print('exiting ' + str(current))
        return False # if we are here, we failed to find a good set of pagoda values...

    '''
        Prints current pagoda values

        RETURNS
        none
    '''  
    def _pagoda_print_state(self):
        predent = " " * self.board_size
        st = predent[1:]
        fwtick = 1
        cnt = 0
        for i in range(self.board_size):
            for j in range(i+1):
                value = (j,i)
                if cnt == fwtick:
                    fwtick += 1
                    cnt = 0
                    st += "\n" + predent[fwtick:]
                st += str(self.pagoda_values[value]) + " "
                cnt += 1

        
        print(st)
    
    