class Board():
    def __init__(self,board_size=4, initial_state_positions=[(0,0)], goal_state_positions=[(0,0)]):
        self.board_size = board_size

        self.initial_state_positions = initial_state_positions
        self.goal_state_positions = goal_state_positions

        # set up board maps and everything necessary for identifying individual cells on a board
        self._alphabetic_values = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.skew_board = [(i,j) for i in range(self.board_size) for j in range(i,self.board_size)]
        self.alphanumeric_board = [self._alphabetic_values[pair[0]] + str(pair[1]+1) for pair in self.skew_board]
        self.board_map = dict(zip(self.skew_board,self.alphanumeric_board))

        # set current state (mutable) and goal state of board (immutable)
        self.board_state = dict(zip(self.skew_board,[1] * len(self.skew_board)))
        self.goal_state = dict(zip(self.skew_board,[0] * len(self.skew_board)))


        self.hash_skew_board = set(self.skew_board)


        self.stack = []

        # "remove peg" from position by setting value to 0
        for position in self.initial_state_positions:
            self.board_state[position] = 0
        for position in self.goal_state_positions:
            self.goal_state[position] = 1
        self.positions_list = []

        self._map_positions()

    def _validate_position(self,position):
        return position[0] in self.hash_skew_board and position[1] in self.hash_skew_board and position[2] in self.hash_skew_board

    def _map_positions(self):
        for i in range(0,self.board_size):
            for j in range(i,self.board_size):
                # locate all possible positions relative to a center cell at (i,j)
                horizontal_position = [(i-1,j),(i,j),(i+1,j)]
                left_diagonal_position = [(i,j-1),(i,j),(i,j+1)]
                right_diagonal_position = [(i-1,j-1),(i,j),(i+1,j+1)]

                # validate each found position to ensure that only valid positions are added
                # a valid position is one with no cells 
                if self._validate_position(horizontal_position):
                    self.positions_list.append(horizontal_position)
                if self._validate_position(left_diagonal_position):
                    self.positions_list.append(left_diagonal_position)                    
                if self._validate_position(right_diagonal_position):
                    self.positions_list.append(right_diagonal_position)

    def jump(self,position):
        self.board_state[position[0]] ^= 1
        self.board_state[position[1]] ^= 1
        self.board_state[position[2]] ^= 1           
    
    