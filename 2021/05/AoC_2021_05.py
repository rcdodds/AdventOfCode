# Standard functionality
from functools import lru_cache
import re
import itertools
import datetime
import json
from collections import Counter

# Additional libraries
import pandas as pd
import numpy as np

# Advent of Code libraries
from aocd.models import Puzzle
from aocd import submit


class InvalidPuzzleTypeError(Exception):
    """Raised when trying to work with a puzzle type that doesn't exist"""
    pass


def split_row(row_string):
    point_a = row_string.split(' -> ')[0]
    point_b = row_string.split(' -> ')[1]

    return point_a, point_b


def split_point(point_coords):
    x_coord = int(point_coords.split(',')[0])
    y_coord = int(point_coords.split(',')[1])

    return x_coord, y_coord


def plot_line(start_x, start_y, end_x, end_y):
    # List of tuples representing points
    points = []

    if start_x == end_x:
        x_step = 0
    elif start_x > end_x:
        x_step = -1
    else:
        x_step = 1

    if start_y == end_y:
        y_step = 0
    elif start_y > end_y:
        y_step = -1
    else:
        y_step = 1

    point = (start_x, start_y)
    delta = (x_step, y_step)
    end = (end_x, end_y)
    points.append(point)

    while point != end:
        point = tuple(map(sum, zip(point, delta)))
        points.append(point)

    return points


def solve_puzzle(pzl_data, letter):
    # All points drawn
    points_covered_by_line = []
    # pzl_data = ['1,1 -> 5,5', '1,5 -> 5,1']

    # Parse inputs
    for line_str in pzl_data:  # 0,9 -> 5,9
        print('Drawing line {} of {}'.format(pzl_data.index(line_str)+1, len(pzl_data)))
        from_pt, to_pt = split_row(line_str)  # 0,9 // 5,9
        from_x, from_y = split_point(from_pt)  # 0 // 9
        to_x, to_y = split_point(to_pt)  # 5 // 9

        # Draw lines according to puzzle logic
        if letter == 'A':
            if from_x == to_x or from_y == to_y:
                points_covered_by_line.extend(plot_line(from_x, from_y, to_x, to_y))
        elif letter == 'B':
            points_covered_by_line.extend(plot_line(from_x, from_y, to_x, to_y))
        else:
            # Invalid letter submitted
            print('Gasp! You tried to use a puzzle type that does not exist.')
            raise InvalidPuzzleTypeError

    # Determine how many points are covered twice
    duplicate_points = [d for d, count in Counter(points_covered_by_line).items() if count > 1]
    return len(duplicate_points)


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 5)
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
            guess = solve_puzzle(puzzle_data, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
