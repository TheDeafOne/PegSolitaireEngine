from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board
from visualization.webapp.webapp_visualizer import WebappVisualizer
from visualization.console.console_visualizer import ConsoleVisualizer
import time


def main():
    print('enter w for webapp, and c for console, note that if you are running this as an exe, the webapp will *not* work')
    response = input("(w)/(c):")
    while response != "w" and response != 'c':
        print('enter w for webapp, and c for console, note that if you are running this as an exe, the webapp will *not* work')
        response = input("(w)/(c):")

    if response == "w":
        WebappVisualizer().visualize()
    else:
        while True:
            while True:
                size_desired = input("Enter Desired Board Size to Test:")
                if size_desired.isnumeric():
                    size_desired = int(size_desired)
                    should_break = False
                    while True:
                        if size_desired < 0 or size_desired > 20:
                            print('size desired must be a number from 1 to 20')
                        else:
                            board = Board(size_desired)
                            backtrack = Backtrack(True)
                            s = time.time()
                            backtrack.backtrack(board)
                            e = time.time()
                            print(
                                f"The length of the Backtrack Solution Stack: {len(backtrack.solution_stack)}")
                            print(
                                f"The time in seconds to find a solution for board size {size_desired}: {e-s}")
                            print("The solution:")
                            ConsoleVisualizer().visualize(backtrack.solution_stack, board.board_size)
                            should_break = True
                        break
                    if should_break:
                        break
                else:
                    print('size must be a number from 1 to 20')


if __name__ == "__main__":
    main()
