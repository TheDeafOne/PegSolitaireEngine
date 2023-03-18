class ConsoleVisualizer:
    def visualize(self, solution_stack, board_size):
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