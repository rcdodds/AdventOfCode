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


class OctopusField:
    def __init__(self, start_array):
        self.field = start_array
        self.flash_count = 0
        self.rounds_played = 0
        self.all_flash = False

    def play_round(self):
        # Log round played
        self.rounds_played += 1

        # Add one to all octopuses
        new_field = self.field + 1
        old_field = self.field

        # Continue flashing octopuses until the field stabilizes
        while True:
            # Find positions of any new flashes
            flash_mask = (new_field > 9) * (old_field <= 9)

            if flash_mask.any():
                # Create array of increases in value due to flashes
                flashes = np.zeros(flash_mask.shape).astype(int)
                # flashes = np.pad(flashes, pad_width=2, mode='constant', constant_values=0)  # Pad to avoid index issues

                # For each flash position, increment the values in a 3x3 square
                for index, flash in np.ndenumerate(flash_mask):
                    if flash:
                        row_min = max(index[0] - 1, 0)
                        row_max = index[0] + 2
                        col_min = max(index[1] - 1, 0)
                        col_max = index[1] + 2

                        flashes[row_min:row_max, col_min:col_max] += 1

                # Before adding new flashes, store field for next comparison
                old_field = new_field
                new_field = old_field + flashes

            # No more flashing - store & exit
            else:
                # Count number of flashes
                self.flash_count += np.sum(new_field > 9)

                # Check whether every octopus flashed
                if np.sum(new_field > 9) == 100:
                    self.all_flash = True

                # Reset anything that flashed to 0
                new_field[new_field > 9] = 0
                self.field = new_field

                # Exit
                break


def solve_puzzle(pzl_data, letter):
    # Starting array
    octopus = OctopusField(np.array(pzl_data))

    if letter == 'A':
        for r in range(100):
            octopus.play_round()
        return octopus.flash_count

    elif letter == 'B':
        while not octopus.all_flash:
            octopus.play_round()
        return octopus.rounds_played

    else:
        raise InvalidPuzzleTypeError(letter)


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 11)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    # puzzle_data = '5483143223\n2745854711\n5264556173\n6141336146\n6357385478\n4167524645\n2176841721\n6882881134\n4846848554\n5283751526'
    puzzle_data = puzzle_data.split('\n')
    puzzle_data = [list(map(int, list(row))) for row in puzzle_data]

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
