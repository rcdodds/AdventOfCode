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


def play_round_smart(last_occurences):
    latest_round = max(list(last_occurences['latest_round'].values()))
    latest_number = list(last_occurences['latest_round'].keys())[list(last_occurences['latest_round'].values()).index(latest_round)]

    try:
        next_num = latest_round - last_occurences['earlier_round'][latest_number]
    except KeyError:
        next_num = 0

    return next_num


def play_round_naive(previous_numbers):
    # Reverse list to deal with most recent occurrences
    previous_numbers.reverse()

    # Extract the most recent number
    last_number_spoken = previous_numbers[0]

    # Attempt to find the most recent occurrence
    try:
        most_recent_occurrence = previous_numbers[1:].index(last_number_spoken) + 1
        next_number = most_recent_occurrence
    except ValueError:
        next_number = 0

    # Clean up
    previous_numbers.reverse()

    return next_number


def solve_puzzle(pzl_data, letter):
    if letter == 'A':
        number_list = pzl_data[:]
        while len(number_list) < 2020:
            number_list.append(play_round_naive(number_list))
            print('Numbers Spoken = {}'.format(len(number_list)))
        return number_list[-1]

    elif letter == 'B':
        number_dict = {'earlier_round': {}, 'latest_round': {number: pzl_data.index(number) + 1 for number in pzl_data}}
        latest_round = max(list(number_dict['latest_round'].values()))
        new_num = pzl_data[-1]
        while latest_round < 30000000:
            new_num = play_round_smart(number_dict)
            latest_round += 1

            try:
                # Move the most recent occurrence to the earlier occurrence
                number_dict['earlier_round'][new_num] = number_dict['latest_round'][new_num]
                # Store this latest round
                number_dict['latest_round'][new_num] = latest_round

            # KeyError indicates this number has not been spoken previously
            except KeyError:
                # Add a new number to the dictionary the inner dictionary
                number_dict['latest_round'][new_num] = latest_round

            print('Numbers Spoken = {}'.format(latest_round))
        return new_num

    else:
        # Invalid letter submitted
        print('Gasp! You tried to use a puzzle type that does not exist.')
        raise InvalidPuzzleTypeError


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2020, 15)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = False

    # Format puzzle input
    puzzle_data = [int(x) for x in puzzle_data.split(',')]
    puzzle_data = [0, 3, 6]
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
            if ready_to_solve and guess:
                submit(guess, part=part, year=year, day=day)
