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


class FishSchool:
    def __init__(self, start_values, min_value, max_value, reset_value):
        # Initialize timer counts with counts of each possible value
        self.timer_counts = {key: start_values.count(key) for key in range(min_value, max_value + 1)}

        # Other variables
        self.birth_time = min_value
        self.new_time = max_value
        self.reset_time = reset_value

    def calc_total(self):
        # Total number of fish is the sum of all values in the counts dictionary
        return sum(self.timer_counts.values())

    def simulate_day(self):
        # Number of fish that have reached minimum time left
        births = self.timer_counts[0]

        # Age all fish a day. Temporarily leaves the highest count alone.
        for timer_key in list(self.timer_counts.keys())[:-1]:
            self.timer_counts[timer_key] = self.timer_counts[timer_key + 1]

        # Each fish that reached minimum has now reset AND births a new fish
        self.timer_counts[self.new_time] = births      # Overwrite (don't add) the hig
        self.timer_counts[self.reset_time] += births    # Add


def solve_puzzle(initial_state, letter):
    # Common steps
    min_fish = 0
    new_fish = 8
    reset_fish = 6
    school = FishSchool(initial_state, min_fish, new_fish, reset_fish)

    if letter == 'A':
        rounds = 80
    elif letter == 'B':
        rounds = 256
    else:
        raise InvalidPuzzleTypeError(letter)

    for r in range(rounds):
        school.simulate_day()

    return school.calc_total()


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 6)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    puzzle_data = puzzle_data.split(',')
    puzzle_data = [int(puzzle_string) for puzzle_string in puzzle_data]
    # puzzle_data = [3, 4, 3, 1, 2]

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
