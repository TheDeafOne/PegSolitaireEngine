class Board():
    def __init__(self,board_size):
        self._alphabetic_values = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.board_size = board_size
        self.alphanumeric_board = [[self._alphabetic_values[i] + str(j) for j in range(i,self.board_size)] for i in range(self.board_size)]
    def test(self):
        print(self.alphanumeric_board)

if __name__ == '__main__':
    b = Board(6)
    b.test()