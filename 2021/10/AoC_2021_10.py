# Standard functionality
from functools import lru_cache
import re
import itertools
import datetime
import json

# Additional libraries
import pandas as pd
import numpy as np

# Advent of Code libraries
from aocd.models import Puzzle
from aocd import submit


class InvalidPuzzleTypeError(Exception):
    """Raised when trying to work with a puzzle type that doesn't exist"""
    def __init__(self, attempted):
        pass


def solve_puzzle(pzl_data, letter):
    # Common steps

    if letter == 'A':
        # Logic for just part A
        return 0

    elif letter == 'B':
        # Logic for just part B
        return 0

    else:
        raise InvalidPuzzleTypeError(letter)


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2020, 10)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = False

    # Format puzzle input
    puzzle_data = puzzle_data.split('\n')
    # puzzle_data = [int(puzzle_string) for puzzle_string in puzzle_data]

    # Consider both puzzles
    for part in ['A', 'B']:
        # If puzzle is not already solved...
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(puzzle_data, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
