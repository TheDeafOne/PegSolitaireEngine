class ConsoleVisualizer:
    '''
    Visualizes a given solution to a board

    PARAMS
    solutions_stack: the list of jumps made to get from the initial state to the goal state
    board_size: the size of the board that has been solved
    '''
    def visualize(self, solution_stack, board_size):
        # cycle through the states and dynamically add whitespace to represent the triangular shape of the board
        for state in solution_stack:
            predent = " " * board_size
            st = predent[1:]
            fwtick = 1
            cnt = 0
            for i in range(board_size):
                for j in range(i+1):
                    value = (j,i)
                    if cnt == fwtick:
                        fwtick += 1
                        cnt = 0
                        st += "\n" + predent[fwtick:]
                    st += str(state[value]) + " "
                    cnt += 1
            print(st)