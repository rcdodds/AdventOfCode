# Standard functionality
from functools import lru_cache
import re
from itertools import chain, combinations
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
    pass


def power_set(iterable, min_elem):
    """powerset([1,2,3], 2) --> (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(min_elem, len(s) + 1))


@lru_cache(200)
def plan_path(path_elements):
    print('Finding valid paths for: {}'.format(str(path_elements)))
    # Valid paths through elements
    valid_paths = 0

    # Loop through elements
    # for pe, path_element in enumerate(path_elements):
    # Find all options for next element
    current_el = path_elements[0]
    next_element_options = [next_el for next_el in path_elements[1:4] if (next_el - current_el) < 4]

    # Loop through the options (only between 0 - 3) for the next element
    for ne, next_element in enumerate(next_element_options):
        # If complete path has been made, add to count
        if next_element == path_elements[-1]:
            valid_paths += 1
        # Otherwise, find all paths from the next element to the end
        else:
            valid_paths += plan_path(path_elements[ne + 1:])

    return valid_paths


def solve_puzzle(pzl_data, letter):
    # Common steps
    pzl_data.sort()  # Sort adaptors in increasing order
    pzl_data.insert(0, 0)  # Add outlet to beginning
    pzl_data.append(max(pzl_data) + 3)  # Add device to end

    if letter == 'A':
        # Get list of the differences at each stage
        differences = [pzl_data[x] - pzl_data[x - 1] for x in range(1, len(pzl_data))]

        return differences.count(1) * differences.count(3)

    elif letter == 'B':
        # Find all valid paths from outlet > device
        return plan_path(tuple(pzl_data))

    else:
        # Invalid letter submitted
        print('Gasp! You tried to use a puzzle type that does not exist.')
        raise InvalidPuzzleTypeError


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2020, 10)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    # puzzle_data = '\n'.join([str(i) for i in [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]])
    puzzle_solution = {'A': {'solved': puzzle.answered_a},
                       'B': {'solved': puzzle.answered_b}}
    ready_to_solve = True

    # Format puzzle input
    delim = '\n'
    cast_int = True
    puzzle_data = puzzle_data.split('\n')
    if cast_int:
        puzzle_data = [int(num_str) for num_str in puzzle_data]

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
