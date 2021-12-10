from aocd.models import Puzzle
from aocd import get_data, submit
import pandas as pd
import numpy as np
import datetime
import json
import parse
import re


def split_input(input_str, cast_int):
    if cast_int:
        return [int(s) for s in input_str.split('\n')]
    else:
        return [s.replace('\n', ' ') for s in input_str.split('\n\n')]


def puzzle_a(input_a):
    valid_entries = 0

    base = r'^{}'
    expr = '(?=.*{})'
    required_fields = ['iyr:', 'byr:', 'eyr:', 'hgt:', 'hcl:', 'ecl:', 'pid']
    regex_string = base.format(''.join(expr.format(w) for w in required_fields))
    regexp = re.compile(regex_string)
    print(regex_string)

    for entry in input_a:
        if regexp.search(entry):
            valid_entries += 1

    return valid_entries


def puzzle_b(input_b):
    valid_entries = 0
    regex_string = r'^(?=.*byr:(19[2-9][0-9]|200[0-2])(\s|$))' \
                   r'(?=.*iyr:20(1[0-9]|20)(\s|$))' \
                   r'(?=.*eyr:20(2[0-9]|30)(\s|$))' \
                   r'(?=.*hgt:((1[5-8][0-9]|19[0-3])cm|(59|6[0-9]|7[0-6])in)(\s|$))' \
                   r'(?=.*hcl:#([0-9]|[a-f]){6}(\s|$))' \
                   r'(?=.*ecl:(amb|blu|brn|gry|grn|hzl|oth)(\s|$))' \
                   r'(?=.*pid:[0-9]{9}(\s|$))'
    regexp = re.compile(regex_string)

    for entry in input_b:
        print(entry)
        if regexp.search(entry):
            valid_entries += 1
        # else:
        #     print('INVALID -- ' + entry)

    return valid_entries


if __name__ == '__main__':
    # Set puzzle of interest
    year = 2020
    day = 4

    # Get puzzle inputs
    puzzle = Puzzle(year=year, day=day)
    puzzle_input = split_input(get_data(year=year, day=day, block=True), cast_int=False)
    print(puzzle_input)

    # Solve puzzles
    puzzle_a_result = puzzle_a(puzzle_input)
    puzzle_b_result = puzzle_b(puzzle_input)

    ready = True
    print('Guess for puzzle A: ' + str(puzzle_a_result))
    print('Guess for puzzle B: ' + str(puzzle_b_result))
    if ready:
        # Attempt to submit guess for puzzle A
        if not puzzle.answered_a and puzzle_a_result != 0:
            if puzzle_a_result not in puzzle.incorrect_answers_a.values():
                submit(puzzle_a_result, part='a', year=year, day=day)
            else:
                print('Guess for puzzle A was previously attempted: {}'.format(puzzle_a_result))

        # Attempt to submit guess for puzzle B
        if not puzzle.answered_b and puzzle_b_result != 0:
            if puzzle_b_result not in puzzle.incorrect_answers_b.values():
                submit(puzzle_b_result, part='b', year=year, day=day)
            else:
                print('Guess for puzzle B was previously attempted: {}'.format(puzzle_b_result))
