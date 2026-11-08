"""Solve the standard board and render its actual states, without a browser."""

import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from algorithms.backtracking.backtracking import Backtrack
from board_logic.board import Board


def render(state, index, total, previous=None):
    scale = 2
    image = Image.new('RGB', (640 * scale, 650 * scale), '#f5f1e8')
    draw = ImageDraw.Draw(image)
    font = lambda size: ImageFont.load_default(size=size * scale)
    point = lambda xy: tuple(round(value * scale) for value in xy)
    box = lambda xy: tuple(round(value * scale) for value in xy)
    draw.text(point((34, 28)), 'Peg Solitaire Engine', fill='#173e50', font=font(30))
    draw.text(point((34, 74)), 'Five rows. Fourteen pegs to one.', fill='#51626a', font=font(18))
    draw.rounded_rectangle(box((32, 112, 608, 594)), radius=18 * scale, fill='#e5c393')
    draw.polygon([point(p) for p in [(320, 137), (72, 557), (568, 557)]], fill='#bd8d53')
    changed = {cell for cell in state if previous is not None and state[cell] != previous[cell]}
    for (x, y), occupied in state.items():
        cx, cy = 320 + (x - y / 2) * 90, 182 + y * 82
        draw.ellipse(box((cx - 23, cy - 21, cx + 23, cy + 25)), fill='#805e3c')
        color = '#225e70' if occupied else '#62452d'
        if occupied and (x, y) in changed:
            color = '#f5c65d'
        draw.ellipse(box((cx - 21, cy - 23, cx + 21, cy + 19)), fill=color)
        if occupied:
            draw.ellipse(box((cx - 12, cy - 16, cx - 3, cy - 9)), fill='#90bac0')
        elif (x, y) in changed:
            draw.ellipse(box((cx - 23, cy - 25, cx + 23, cy + 21)), outline='#efb08a', width=3 * scale)
    remaining = sum(state.values())
    label = 'Initial board' if index == 0 else f'Jump {index} of {total}'
    if index == total:
        label += ' - solved'
    draw.text(point((34, 612)), label, fill='#173e50', font=font(20))
    draw.text(point((478, 613)), f'{remaining} peg' + ('' if remaining == 1 else 's'),
              fill='#51626a', font=font(18))
    return image.resize((640, 650), Image.Resampling.LANCZOS)


def main():
    board = Board()
    initial = board.board_state.copy()
    solver = Backtrack(use_pagoda=True)
    path = solver.backtrack(board)
    assert solver.did_solve and len(path) == 13
    states = [initial] + path
    for previous, current in zip(states, states[1:]):
        changes = {cell for cell in current if current[cell] != previous[cell]}
        legal = [move for move in board.positions_list if set(move) == changes
                 and tuple(previous[cell] for cell in move) in ((1, 1, 0), (0, 1, 1))]
        assert len(legal) == 1
        assert sum(previous.values()) - sum(current.values()) == 1
    assert states[-1] == board.goal_state
    frames = [render(state, index, len(path), states[index - 1] if index else None)
              for index, state in enumerate(states)]
    destination = ROOT / 'docs'
    destination.mkdir(exist_ok=True)
    frames[0].save(destination / 'initial-board.png')
    frames[-1].save(destination / 'solved-board.png')
    frames[0].save(destination / 'solution.gif', save_all=True, append_images=frames[1:],
                   duration=[1800] + [850] * (len(frames) - 2) + [2500], loop=0,
                   optimize=True, disposal=2)
    (destination / 'solution.json').write_text(json.dumps({
        'board_size': 5, 'initial_hole': [0, 0], 'goal': [0, 0],
        'use_pagoda': True, 'jumps': len(path),
        'states': [{f'p{x}-{y}': occupied for (x, y), occupied in state.items()}
                   for state in states],
    }, indent=2) + '\n')
    print(f'Wrote {len(frames)} checked states ({len(path)} legal jumps) to {destination}')


if __name__ == '__main__':
    main()
