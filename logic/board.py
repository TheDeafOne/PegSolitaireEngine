class Board():
    def __init__(self,board_size=4,board=None):
        self._alphabetic_values = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.board_size = board_size
        if board:
            self._process_board(board)
        else:
            self._initialize_board()
        

    def _process_board(self,board):
        self.board_size = board.board_size
        self.skew_board = board.skew_board
        self.hash_skew_board = board.hash_skew_board
        self.alphanumeric_board = board.alphanumeric_board
        self.board_map = board.board_map
        self.positions_list = board.positions_list
    
    def _initialize_board(self):
        self.skew_board = [(i,j) for i in range(self.board_size) for j in range(i,self.board_size)]
        self.hash_skew_board = set(self.skew_board)
        self.alphanumeric_board = [self._alphabetic_values[pair[0]] + str(pair[1]+1) for pair in self.skew_board]
        self.board_map = dict(zip(self.skew_board,self.alphanumeric_board))
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


if __name__ == '__main__':
    b = Board(5)
    
    