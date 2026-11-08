"""Rule-level and asynchronous-job regressions, using only unittest and Flask."""

from collections import deque
from threading import Event
from time import monotonic
import unittest
from unittest.mock import patch

from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board
from visualization.webapp.webapp_visualizer import AlgorithmManager, WebappVisualizer


def reachable(board):
    """Independent breadth-first reference over bit masks for small boards."""
    cells = board.skew_board
    initial = sum(value << cells.index(cell) for cell, value in board.board_state.items())
    goal = sum(value << cells.index(cell) for cell, value in board.goal_state.items())
    moves = [tuple(1 << cells.index(cell) for cell in move)
             for move in board.positions_list]
    todo, seen = deque([initial]), {initial}
    while todo:
        state = todo.popleft()
        if state == goal:
            return True
        for a, b, c in moves:
            if state & b and bool(state & a) != bool(state & c):
                new = state ^ (a | b | c)
                if new not in seen:
                    seen.add(new)
                    todo.append(new)
    return False


class SolverChecks(unittest.TestCase):
    def test_standard_solution_every_jump_is_legal(self):
        board = Board()
        previous = board.board_state.copy()
        solver = Backtrack(True)
        states = solver.backtrack(board)
        self.assertTrue(solver.did_solve)
        self.assertTrue(solver.finished)
        self.assertEqual(len(states), 13)
        for state in states:
            changed = {cell for cell in state if state[cell] != previous[cell]}
            candidates = [move for move in board.positions_list if set(move) == changed]
            self.assertEqual(len(candidates), 1)
            self.assertIn(tuple(previous[cell] for cell in candidates[0]),
                          ((1, 1, 0), (0, 1, 1)))
            self.assertEqual(sum(previous.values()) - sum(state.values()), 1)
            previous = state
        self.assertEqual(previous, board.goal_state)

    def test_all_three_row_states_and_goals_match_reference(self):
        # Exercises asymmetric goals, pagoda equality, and reused solver state.
        for pagoda in (False, True):
            solver = Backtrack(pagoda)
            for mask in range(64):
                for goal in Board(3).skew_board:
                    board = Board(3, [], [goal])
                    board.board_state = {cell: (mask >> i) & 1
                                         for i, cell in enumerate(board.skew_board)}
                    initial = board.board_state.copy()
                    expected = reachable(board)
                    solver.backtrack(board)
                    self.assertEqual(solver.did_solve, expected, (pagoda, mask, goal))
                    self.assertTrue(solver.finished)
                    if not expected:
                        self.assertEqual(board.board_state, initial)

    def test_cancellation_restores_input(self):
        cancel = Event()
        board = Board()
        initial = board.board_state.copy()
        solver = Backtrack(False, cancel_event=cancel,
                           on_state=lambda state: cancel.set())
        self.assertFalse(solver.backtrack(board))
        self.assertTrue(solver.cancelled)
        self.assertTrue(solver.finished)
        self.assertEqual(board.board_state, initial)
        self.assertEqual(solver.solution_stack, [])

    def test_invalid_coordinate_rejected(self):
        with self.assertRaises(ValueError):
            Board(5, [(5, 0)])


class WebChecks(unittest.TestCase):
    def setUp(self):
        self.manager = AlgorithmManager()

    def wait(self, job_id):
        self.manager.jobs[job_id].thread.join(3)
        self.assertFalse(self.manager.jobs[job_id].thread.is_alive())
        return self.manager.poll(job_id)

    def test_unsolvable_finishes_and_poll_never_waits_for_success(self):
        # Two occupied cells on a two-row board have no legal jump.
        job_id = self.manager.start(2, 'p0-0', 'p0-0')
        self.assertEqual(self.wait(job_id)['status'], 'unsolved')
        started = monotonic()
        self.assertEqual(self.manager.poll(job_id)['status'], 'unsolved')
        self.assertLess(monotonic() - started, 0.1)

    def test_new_job_does_not_replace_old_board_or_worker(self):
        first = self.manager.start(5, 'p0-0', 'p0-0', True)
        second = self.manager.start(2, 'p0-0', 'p1-1')
        self.assertNotEqual(first, second)
        self.assertEqual(self.wait(second)['status'], 'unsolved')
        self.manager.cancel(first)
        self.assertEqual(self.wait(first)['status'], 'cancelled')
        self.assertEqual(self.manager.poll(second)['status'], 'unsolved')
        self.assertEqual(len(self.manager.poll(first)['state']), 15)
        self.assertEqual(len(self.manager.poll(second)['state']), 3)

    def test_worker_exception_becomes_error(self):
        with patch.object(Backtrack, 'backtrack', side_effect=RuntimeError('example error')):
            job_id = self.manager.start(3, 'p0-0', 'p0-0')
            result = self.wait(job_id)
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['error'], 'example error')

    def test_http_validation_and_solved_response(self):
        client = WebappVisualizer.app.test_client()
        self.assertEqual(client.get('/').status_code, 200)
        self.assertEqual(client.get('/run/5/p5-0/p0-0/false').status_code, 400)
        self.assertEqual(client.get('/run/0/p0-0/p0-0/false').status_code, 400)
        self.assertEqual(client.get('/poll?job_id=unknown').status_code, 404)
        started = client.get('/run/5/p0-0/p0-0/false')
        self.assertEqual(started.status_code, 200)
        job_id = started.json['job_id']
        import visualization.webapp.webapp_visualizer as web
        web.manager.jobs[job_id].thread.join(3)
        result = client.get('/poll', query_string={'job_id': job_id})
        self.assertEqual(result.json['status'], 'solved')
        self.assertEqual(len(result.json['states']), 13)
        self.assertEqual(sum(result.json['state'].values()), 1)


if __name__ == '__main__':
    unittest.main()
