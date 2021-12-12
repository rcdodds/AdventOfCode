# Libraries
import numpy as np
from aocd.models import Puzzle
from aocd import submit


def solve_puzzle(pzl_data, letter):

    if letter == 'A':
        return 0

    elif letter == 'B':
        return 0


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 12)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = False

    # Format puzzle input
    puzzle_data = puzzle.input_data.split('\n')

    # Consider both puzzles
    for part in ['A', 'B']:
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(puzzle_data, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
