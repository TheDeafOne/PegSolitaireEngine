from .backtracking.backtracking import Backtrack
class Algorithms:
    def backtrack(self, board, live=False):
        if live:
            # manage live backtracking feed
            pass
        else:
            backtracking = Backtrack()
            backtracking.backtrack(board)
            return backtracking
        