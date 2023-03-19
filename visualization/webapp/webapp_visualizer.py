from flask import Flask, render_template
from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board
from threading import Thread
import time

board = None
class AlgorithmManager: 
    def set_board(self,board_size, initial_state, goal_state):
        board_size = int(board_size)
        initial_state = self._parse_state(initial_state)
        goal_state = self._parse_state(goal_state)
        global board
        board = Board(board_size,[initial_state],[goal_state])
        self.run_live = False
        self.backtrack = Backtrack(True, self.run_live)

    
    def _parse_state(self,state):
        return tuple(map(int,state[1:].split('-')))
    
    def start_backtracking(self,run_live):
        self.run_live = run_live
        if self.run_live:
            self.backtrack = Backtrack(True, True)
        self.backtrack.backtrack(board)
    
    def get_next_state(self):
        if self.run_live:
            self.backtrack.next_step = True
            if self.backtrack.solution_stack:
                return self.backtrack.solution_stack[-1]
            return []
        else:
            while not self.backtrack.did_solve:
                time.sleep(0.1)
            return self.backtrack.solution_stack
        


manager = AlgorithmManager()
algo_thread: Thread


class WebappVisualizer:
    app = Flask(__name__)
    def visualize(self):
        self.app.run(debug=True)

    @app.route('/')
    def _run_app():
        return render_template('main.html', chr=chr)

    @app.route('/run/<board_size>/<initial_state>/<goal_state>/<run_live>')
    def run(board_size, initial_state, goal_state, run_live):
        manager.set_board(board_size,initial_state,goal_state)
        global algo_thread
        algo_thread = Thread(target=manager.start_backtracking,args=[run_live=="true"])
        algo_thread.start()
        return "GOOD"
      
    @app.route('/poll')
    def get_next_state():   
        data = manager.get_next_state()  
        ret = []   
        if manager.run_live:
            ret = {}
            for cell in data:
                ret['p'+str(cell)[1:-1].replace(', ','-')] = data[cell]  
        else:
            for board_state in data:
                new_board_state = {}
                for cell in board_state:
                    new_board_state['p'+str(cell)[1:-1].replace(', ','-')] = board_state[cell]
                ret.append(new_board_state)
        return ret
