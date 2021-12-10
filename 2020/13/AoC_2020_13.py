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
from aoc_util import ChineseRemainderTheorem as crt


class InvalidPuzzleTypeError(Exception):
    """Raised when trying to work with a puzzle type that doesn't exist"""
    pass


def solve_puzzle(pzl_data, letter):
    # Common steps
    current_timestamp = int(pzl_data[0])
    buses_list = [int(b) if b.isnumeric() else b for b in pzl_data[1].split(',')]
    # for i, x in enumerate(buses_list):
    #     print((len(buses_list)-i-1)%23, x)
    # buses_list = [7, 13, 'x', 'x', 59, 'x', 31, 19]
    # buses_list = [17, 'x', 13, 19]
    # buses_list = [67, 7, 59, 61]
    # buses_list = [67, 'x', 7, 59, 61]
    # buses_list = [67, 7, 'x', 59, 61]
    # buses_list = [1789, 37, 47, 1889]

    if letter == 'A':
        next_depart_timestamps = {}
        # Loop through every bus that is active (integers, not 'x' strings)
        for active_bus in [bus_id for bus_id in buses_list if type(bus_id) == int]:
            most_recent_departure = current_timestamp % active_bus          # e.g. time 10, bus 7 departed 3 min ago
            next_departure_time = active_bus - most_recent_departure        # e.g. bus 7 will depart again in 4 min
            next_depart_timestamps[active_bus] = next_departure_time        # Store in dictionary of departure times

        # Get minimum timestamp of next departure and the associated bus ID
        next_bus = min(next_depart_timestamps, key=next_depart_timestamps.get)
        next_bus_time = min(next_depart_timestamps.values())
        return next_bus * next_bus_time

    elif letter == 'B':
        # Initialize
        bus_array = np.array([b for b in buses_list if type(b) == int])
        offset_array = np.array([(b - buses_list.index(b)) % b for b in buses_list if type(b) == int])

        # Use Chinese Remainder Theorem to determine next timestamp
        next_time, increment = crt.solve_crt(bus_array, offset_array)

        return int(next_time)

    else:
        # Invalid letter submitted
        print('Gasp! You tried to use a puzzle type that does not exist.')
        raise InvalidPuzzleTypeError


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2020, 13)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    puzzle_data = puzzle_data.split('\n')
    # puzzle_data = [int(puzzle_string) for puzzle_string in puzzle_data]

    # Consider both puzzles
    for part in ['A', 'B']:
        # If puzzle is not already solved...
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(tuple(puzzle_data), part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
