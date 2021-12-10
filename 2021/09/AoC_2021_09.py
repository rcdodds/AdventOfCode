# Standard functionality
from functools import lru_cache
import re
import itertools
import datetime
import json

# Additional libraries
import pandas as pd
import numpy as np
import networkx as nx

# Advent of Code libraries
from aocd.models import Puzzle
from aocd import submit
from aoc_util import ArrayExtrema as arr_ext


class InvalidPuzzleTypeError(Exception):
    """Raised when trying to work with a puzzle type that doesn't exist"""
    def __init__(self, attempted):
        pass


def solve_puzzle(pzl_data, letter):
    # Store "field" in numpy array
    input_array = np.array(pzl_data)

    # Locations of minima (boolean mask)
    minima_mask = arr_ext.detect_local_minima(input_array)

    if letter == 'A':
        # Calculate the sum of all minima risk scores
        minima_risks = (input_array + 1) * minima_mask
        return np.sum(minima_risks)
    elif letter == 'B':
        # Find basin sizes for each minima
        return arr_ext.detect_basin_size(input_array)

    else:
        raise InvalidPuzzleTypeError(letter)


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 9)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = False

    # Format puzzle input
    # puzzle_data = '2199943210\n3987894921\n9856789892\n8767896789\n9899965678'
    puzzle_data = puzzle_data.split('\n')
    puzzle_data = [[int(digit) for digit in puzzle_string] for puzzle_string in puzzle_data]

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
