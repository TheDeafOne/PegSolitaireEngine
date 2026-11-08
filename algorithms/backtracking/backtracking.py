"""Depth-first search with failed-state memoization and optional pagoda pruning."""

from threading import Event

from board_logic.board import Board
from ..pagoda.pagoda import PagodaGenerator


class Backtrack:
    def __init__(self, use_pagoda=False, is_game_loop=False, cancel_event=None,
                 on_state=None):
        self.use_pagoda = use_pagoda
        self.is_game_loop = is_game_loop
        self.cancel_event = cancel_event if cancel_event is not None else Event()
        self.on_state = on_state
        self.pagoda_generator = PagodaGenerator()
        self.solution_stack = []
        self.termination_states = set()
        self.pagoda_function = {}
        self.did_solve = False
        self.finished = False
        self.cancelled = False
        self.states_examined = 0

    def backtrack(self, board: Board):
        """Return the path after each jump, or False if unsolved/cancelled.

        The board finishes at the goal on success and is restored otherwise.
        A solver can be reused: all search-specific state is reset here.
        """
        self.solution_stack = []
        self.termination_states = set()
        self.pagoda_function = {}
        self.did_solve = False
        self.finished = False
        self.cancelled = False
        self.states_examined = 0
        try:
            if self.use_pagoda:
                self.pagoda_function = self.pagoda_generator.generate_pagoda_function(
                    board, self.cancel_event)
            self.goal_weight = sum(self.pagoda_function.get(cell, 0)
                                   for cell, occupied in board.goal_state.items()
                                   if occupied)
            self.did_solve = self._search(board)
            return self.solution_stack if self.did_solve else False
        finally:
            self.cancelled = self.cancel_event.is_set()
            self.finished = True

    def _search(self, board):
        if self.cancel_event.is_set():
            return False
        self.states_examined += 1
        if board.board_state == board.goal_state:
            return True

        key = board.get_board_string()
        # A rotated failure need not be a failure for the same fixed goal.
        # Only memoize exact states, keeping arbitrary goal selections sound.
        if key in self.termination_states:
            return False
        if sum(board.board_state.values()) <= sum(board.goal_state.values()):
            return False
        if self.pagoda_function:
            weight = sum(self.pagoda_function[cell]
                         for cell, occupied in board.board_state.items() if occupied)
            # Legal jumps cannot increase the pagoda sum. Equality is allowed.
            if weight < self.goal_weight:
                self.termination_states.add(key)
                return False

        for position in board.positions_list:
            values = tuple(board.board_state[cell] for cell in position)
            if values not in ((1, 1, 0), (0, 1, 1)):
                continue
            board.jump(position)
            self.solution_stack.append(board.board_state.copy())
            if self.on_state is not None:
                self.on_state(board.board_state.copy())
            if self.is_game_loop:
                self.cancel_event.wait(0.03)
            if self._search(board):
                return True
            board.jump(position)
            self.solution_stack.pop()
            if self.on_state is not None:
                self.on_state(board.board_state.copy())
            if self.cancel_event.is_set():
                return False

        self.termination_states.add(key)
        return False
