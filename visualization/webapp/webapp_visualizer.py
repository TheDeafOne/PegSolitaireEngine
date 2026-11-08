"""A small asynchronous visualizer; each run owns its board and solver."""

from dataclasses import dataclass, field
from threading import Event, Lock, Thread
from uuid import uuid4

from flask import Flask, jsonify, render_template, request

from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board


def serialize(state):
    return {f'p{x}-{y}': value for (x, y), value in state.items()}


@dataclass
class SearchJob:
    board: Board
    live: bool
    status: str = 'running'
    error: str = ''
    states: list = field(default_factory=list)
    current: dict = field(default_factory=dict)
    cancel: Event = field(default_factory=Event)
    lock: Lock = field(default_factory=Lock)
    thread: Thread = None


class AlgorithmManager:
    def __init__(self):
        self.jobs = {}
        self.lock = Lock()

    @staticmethod
    def _parse_state(state):
        if not state.startswith('p'):
            raise ValueError('select an initial hole and a goal cell')
        try:
            x, y = map(int, state[1:].split('-'))
            return x, y
        except (ValueError, TypeError):
            raise ValueError('invalid cell coordinates') from None

    def start(self, board_size, initial_state, goal_state, run_live=False):
        board_size = int(board_size)
        if not 2 <= board_size <= 10:
            raise ValueError('web board size must be between 2 and 10')
        board = Board(board_size, [self._parse_state(initial_state)],
                      [self._parse_state(goal_state)])
        job = SearchJob(board, run_live, current=board.board_state.copy())
        job_id = uuid4().hex
        with self.lock:
            # Retain a small history, without ever evicting an active worker.
            if len(self.jobs) >= 32:
                for old_id, old_job in list(self.jobs.items()):
                    if old_job.status != 'running':
                        del self.jobs[old_id]
                    if len(self.jobs) < 32:
                        break
                if len(self.jobs) >= 32:
                    raise ValueError('too many active searches; cancel a search first')
            self.jobs[job_id] = job
        job.thread = Thread(target=self._solve, args=(job,), daemon=True)
        job.thread.start()
        return job_id

    def _solve(self, job):
        def publish(state):
            with job.lock:
                job.current = state

        solver = Backtrack(True, job.live, job.cancel,
                           publish if job.live else None)
        try:
            solution = solver.backtrack(job.board)
            with job.lock:
                if job.cancel.is_set():
                    job.status = 'cancelled'
                elif solver.did_solve:
                    job.states = solution
                    job.current = job.board.board_state.copy()
                    job.status = 'solved'
                else:
                    job.status = 'unsolved'
        except Exception as exc:
            with job.lock:
                job.status = 'error'
                job.error = str(exc)

    def poll(self, job_id):
        with self.lock:
            job = self.jobs.get(job_id)
        if job is None:
            return None
        with job.lock:
            return {'status': job.status, 'live': job.live,
                    'state': serialize(job.current),
                    'states': [serialize(state) for state in job.states],
                    'error': job.error}

    def cancel(self, job_id):
        with self.lock:
            job = self.jobs.get(job_id)
        if job is None:
            return False
        job.cancel.set()
        return True


manager = AlgorithmManager()


class WebappVisualizer:
    app = Flask(__name__)

    def visualize(self):
        self.app.run(debug=False)

    @app.get('/')
    def index():
        return render_template('main.html')

    @app.get('/run/<board_size>/<initial_state>/<goal_state>/<run_live>')
    def run(board_size, initial_state, goal_state, run_live):
        if run_live not in ('true', 'false'):
            return jsonify(error='live must be true or false'), 400
        try:
            job_id = manager.start(board_size, initial_state, goal_state,
                                   run_live == 'true')
            return jsonify(job_id=job_id)
        except (ValueError, TypeError) as exc:
            return jsonify(error=str(exc)), 400

    @app.get('/poll')
    def poll():
        result = manager.poll(request.args.get('job_id'))
        if result is None:
            return jsonify(error='search not found'), 404
        return jsonify(result)

    @app.post('/cancel/<job_id>')
    def cancel(job_id):
        if not manager.cancel(job_id):
            return jsonify(error='search not found'), 404
        return jsonify(status='cancelling')


if __name__ == '__main__':
    WebappVisualizer().visualize()
