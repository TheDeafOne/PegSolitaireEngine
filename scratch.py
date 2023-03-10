from visualization.vizualizer import Visualizer
from board_logic.board import Board

visualizer = Visualizer()
board = Board(5)
# visualizer.console(board)
visualizer.webapp(board)