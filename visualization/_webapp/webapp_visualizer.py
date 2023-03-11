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
        self.backtrack = Backtrack(True)
    
    def _parse_state(self,state):
        return tuple(map(int,state[1:].split('-')))
    
    def start_backtracking(self):
        self.backtrack.backtrack(board)
    
    def get_next_state(self):
        self.backtrack.next_step = True
        
        if self.backtrack.solution_stack:
            return self.backtrack.solution_stack[-1]
        return []


manager = AlgorithmManager()
algo_thread: Thread


class WebappVisualizer:
    app = Flask(__name__)
    def visualize(self):
        self.app.run(debug=True)

    @app.route('/')
    def _run_app():
        return render_template('main.html', chr=chr)

    @app.route('/run/<board_size>/<initial_state>/<goal_state>')
    def run(board_size, initial_state, goal_state):
        print("inputs: ",board_size,initial_state,goal_state,'\n')
        manager.set_board(board_size,initial_state,goal_state)
        global algo_thread
        algo_thread = Thread(target=manager.start_backtracking)
        algo_thread.start()
        return "GOOD"
      
    @app.route('/poll')
    def get_next_state():   
        data = manager.get_next_state()     
        print('data',data)
        return {'data':'test'}
