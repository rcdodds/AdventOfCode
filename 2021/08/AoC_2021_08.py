# Standard functionality
from functools import lru_cache
import regex as re
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


def find_letter_mapping(in_str):
    # Variables
    standard_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    regex_len2 = r'(\s|^)[a-z]{2}(\s|$)'
    regex_len3 = r'(\s|^)[a-z]{3}(\s|$)'
    regex_len4 = r'(\s|^)[a-z]{4}(\s|$)'

    # Get counts for use in determining letter mappings
    actual_counts = {ch: in_str.count(ch) for ch in standard_letters}

    # Search for what letter is actually letter A (Contained in the string of LEN3 but not LEN2)
    actual_A = (set(re.search(regex_len3, in_str).group()) - set(re.search(regex_len2, in_str).group())).pop()

    # Search for what letter is actually letter B (Only letter that appears exactly 6 times)
    actual_B = list(actual_counts.keys())[list(actual_counts.values()).index(6)]

    # Search for what letter is actually letter E (Only letter that appears exactly 4 times)
    actual_E = list(actual_counts.keys())[list(actual_counts.values()).index(4)]

    # Search for what letter is actually letter C (Contained in LEN2 and appears exactly 8 times)
    appears_8 = set([ch for ch, ct in actual_counts.items() if ct == 8])
    actual_C = set(re.search(regex_len2, in_str).group()).intersection(appears_8).pop()

    # Search for what letter is actually letter F (Contained in LEN2 and appears exactly 9 times)
    appears_9 = set([ch for ch, ct in actual_counts.items() if ct == 9])
    actual_F = set(re.search(regex_len2, in_str).group()).intersection(appears_9).pop()

    # Search for what letter is actually letter D (Contained in LEN4 and not actually B/C/F)
    actual_D = (set(re.search(regex_len4, in_str).group()) - {actual_B, actual_C, actual_F, ' '}).pop()

    # Search for what letter is actually letter G (Only one left)
    actual_G = (set(standard_letters) - {actual_A, actual_B, actual_C, actual_D, actual_E, actual_F}).pop()

    return [actual_A, actual_B, actual_C, actual_D, actual_E, actual_F, actual_G]


def decipher_output_value(out_str, new_letters):
    # Processing variables
    render_number_dict = {
        '0': {'a', 'b', 'c', 'e', 'f', 'g'},
        '1': {'c', 'f'},  # Unique w/ 2 chars
        '2': {'a', 'c', 'd', 'e', 'g'},
        '3': {'a', 'c', 'd', 'f', 'g'},
        '4': {'b', 'c', 'd', 'f'},  # Unique w/ 4 chars
        '5': {'a', 'b', 'd', 'f', 'g'},
        '6': {'a', 'b', 'd', 'e', 'f', 'g'},
        '7': {'a', 'c', 'f'},  # Unique w/ 3 chars (same as #1 + 'a')
        '8': {'a', 'b', 'c', 'd', 'e', 'f', 'g'},  # Unique w/ 7 chars
        '9': {'a', 'b', 'c', 'd', 'f', 'g'}
    }
    normal_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    # Map letters
    new_digit_string = ''
    for ltr in out_str:
        if ltr != ' ':
            new_digit_string = new_digit_string + normal_letters[new_letters.index(ltr)]
        else:
            new_digit_string = new_digit_string + ltr
    out_vals = new_digit_string.split(' ')

    # Find digits
    output_digits = ''
    for out_val in out_vals:
        if out_val:
            output_digit_characters = set(out_val)
            output_digit = list(render_number_dict.keys())[list(render_number_dict.values()).index(output_digit_characters)]
            output_digits = output_digits + output_digit

    return int(output_digits)


def solve_puzzle(pzl_data, letter):
    if letter == 'A':
        unique_lengths = 0
        for row in pzl_data:
            output_str = row.split('|')[-1]
            regex_pattern = r'((\s|^)[a-z]{2}(\s|$))|' \
                            r'((\s|^)[a-z]{4}(\s|$))|' \
                            r'((\s|^)[a-z]{3}(\s|$))|' \
                            r'((\s|^)[a-z]{7}(\s|$))'
            matches = re.findall(regex_pattern, output_str, overlapped=True)
            unique_lengths += len(matches)
        return unique_lengths

    elif letter == 'B':
        total_value = 0
        # Loop through each puzzle
        for row in pzl_data:
            # Split puzzle
            input_str = row.split(' | ')[0]
            output_str = row.split(' | ')[-1]

            actual_letters = find_letter_mapping(input_str)
            total_value += decipher_output_value(output_str, actual_letters)

        return total_value

    else:
        raise InvalidPuzzleTypeError(letter)


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 8)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    puzzle_data = puzzle_data.split('\n')

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
