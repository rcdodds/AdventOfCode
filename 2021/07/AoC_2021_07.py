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


def fuel_to_move_even(start_array, destination):
    return sum(abs(start_array - destination))


def fuel_to_move_increasing(start_arr, dst):
    # Get the move size
    move_sizes = abs(start_arr - dst)

    # 1 + 2 + 3 + ... + n = (n(n+1))/2
    fuel_consumption = 0.5 * move_sizes * (move_sizes + 1)

    return sum(fuel_consumption)


def solve_puzzle(pzl_data, letter):
    # Common steps
    crab_array = np.array(pzl_data)

    if letter == 'A':
        fuel_spent = {dest: fuel_to_move_even(crab_array, dest) for dest in range(min(crab_array), max(crab_array) + 1)}
        return min(list(fuel_spent.values()))

    elif letter == 'B':
        fuel_spent = {dest: fuel_to_move_increasing(crab_array, dest) for dest in range(min(crab_array), max(crab_array) + 1)}
        return int(min(list(fuel_spent.values())))

    else:
        raise InvalidPuzzleTypeError(letter)


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 7)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    puzzle_data = [int(x) for x in puzzle_data.split(',')]

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
