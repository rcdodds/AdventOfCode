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
    pass


def split_instruction(instruction_string):
    return instruction_string[0], int(instruction_string[1:])


def manhattan_distance(x, y):
    return abs(x) + abs(y)


def follow_instruction_a(current_x, current_y, current_heading, instruction):
    # Split instruction
    direction, amount = split_instruction(instruction)

    # Possible headings in CW (right) order starting with East
    possible_headings = ['E', 'S', 'W', 'N']

    # Replace forward with the direction the boat is facing
    if direction == 'F':
        direction = current_heading

    # Move the boat
    if direction == 'N':
        new_x = current_x
        new_y = current_y + amount
        new_heading = current_heading
    elif direction == 'S':
        new_x = current_x
        new_y = current_y - amount
        new_heading = current_heading
    elif direction == 'E':
        new_x = current_x + amount
        new_y = current_y
        new_heading = current_heading
    elif direction == 'W':
        new_x = current_x - amount
        new_y = current_y
        new_heading = current_heading

    # Turn the boat
    elif direction == 'R':
        new_x = current_x
        new_y = current_y
        new_heading = possible_headings[((possible_headings.index(current_heading) * 90 + amount) % 360) // 90]
    elif direction == 'L':
        new_x = current_x
        new_y = current_y
        new_heading = possible_headings[((possible_headings.index(current_heading) * 90 - amount) % 360) // 90]
    else:
        new_x, new_y, new_heading = (current_x, current_y, current_heading)

    # Return new info
    return new_x, new_y, new_heading


def follow_instruction_b(coords, instruction):
    # Split instruction
    direction, amount = split_instruction(instruction)

    # Determine how much to move
    x_offset = coords['waypoint']['x'] - coords['ship']['x']
    y_offset = coords['waypoint']['y'] - coords['ship']['y']

    # Consolidate turn actions

    if direction == 'R' or direction == 'L':
        amount = amount % 360
        if direction == 'R':
            direction = 'L'
            amount = 360 - amount

    # Move the boat
    if direction == 'F':
        coords['waypoint']['x'] = coords['waypoint']['x'] + x_offset * amount
        coords['ship']['x'] = coords['ship']['x'] + x_offset * amount
        coords['waypoint']['y'] = coords['waypoint']['y'] + y_offset * amount
        coords['ship']['y'] = coords['ship']['y'] + y_offset * amount

    # Move the waypoint
    elif direction == 'N':
        coords['waypoint']['y'] = coords['waypoint']['y'] + amount
    elif direction == 'S':
        coords['waypoint']['y'] = coords['waypoint']['y'] - amount
    elif direction == 'E':
        coords['waypoint']['x'] = coords['waypoint']['x'] + amount
    elif direction == 'W':
        coords['waypoint']['x'] = coords['waypoint']['x'] - amount

    # Rotate the waypoint
    else:
        if amount == 90:
            temp = x_offset
            x_offset = y_offset * -1
            y_offset = temp
        elif amount == 180:
            x_offset = x_offset * -1
            y_offset = y_offset * -1
        elif amount == 270:
            temp = x_offset
            x_offset = y_offset
            y_offset = temp * -1

        coords['waypoint']['x'] = coords['ship']['x'] + x_offset
        coords['waypoint']['y'] = coords['ship']['y'] + y_offset

    return coords


def solve_puzzle(pzl_data, pzl_part):
    if pzl_part == 'A':
        (x_coord, y_coord, heading) = (0, 0, 'E')
        for instruction in pzl_data:
            (x_coord, y_coord, heading) = follow_instruction_a(x_coord, y_coord, heading, instruction)

        return manhattan_distance(x_coord, y_coord)

    elif pzl_part == 'B':
        coordinates = {
            'ship': {'x': 0, 'y': 0},
            'waypoint': {'x': 10, 'y': 1},
        }

        for instruction in pzl_data:
            coordinates = follow_instruction_b(coordinates, instruction)
            print(coordinates)

        return manhattan_distance(coordinates['ship']['x'], coordinates['ship']['y'])

    else:
        # Invalid letter submitted
        print('Gasp! You tried to use a puzzle type that does not exist.')
        raise InvalidPuzzleTypeError


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2020, 12)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # puzzle_data = 'F10\nN3\nF7\nR90\nF11'

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
