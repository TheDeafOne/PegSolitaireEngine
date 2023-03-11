from ._console.console_visualizer import ConsoleVisualizer
from ._webapp.webapp_visualizer import WebappVisualizer
from algorithms.algorithms import Algorithms
from board_logic.board import Board

class Visualizer:
    def __init__(self, live=False):
        self._live = live
        self._console_visualizer = ConsoleVisualizer()
        self._webapp_visualizer = WebappVisualizer()
        self._algorithms = Algorithms()
        
    def console(self, board: Board):
        if self._live:
            # live visualize on console
            # included backtracking
            
            pass
        else:
            # visualize on console, just solution stack, no backtracking
            solution_stack = self._algorithms.backtrack(board).solution_stack
            self._console_visualizer.visualize(solution_stack,board.board_size)
    
    def webapp(self):
        self._webapp_visualizer.visualize()
        
