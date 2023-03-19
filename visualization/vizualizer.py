from ._console.console_visualizer import ConsoleVisualizer
from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board

class Visualizer:
    def __init__(self, live=False):
        self._live = live
        self._console_visualizer = ConsoleVisualizer()
        
    def console(self, board: Board, backtrack: Backtrack):
        if self._live:
            # live visualize on console
            # included backtracking
            pass
        else:
            # visualize on console, just solution stack, no backtracking
            solution_stack = backtrack.backtrack(board)
            self._console_visualizer.visualize(solution_stack,board.board_size)
