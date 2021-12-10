from aocd.models import Puzzle
from aocd import get_data, submit
import pandas as pd
import numpy as np
import datetime
import json
import parse
import re


def split_input(input_str, cast_int, split_blanks):
    if split_blanks:
        delim = '\n\n'
    else:
        delim = '\n'

    if cast_int:
        return [int(s) for s in input_str.split(delim)]
    else:
        return input_str.split(delim)


def puzzle_a(input_a):
    zipped_digits = zip(*input_a)

    g_rate = ''
    e_rate = ''

    for digit_list in zipped_digits:
        if digit_list.count('0') > digit_list.count('1'):
            g_rate = g_rate + '0'
            e_rate = e_rate + '1'
        else:
            g_rate = g_rate + '1'
            e_rate = e_rate + '0'

    return int(g_rate,2) * int(e_rate,2)


def puzzle_b(input_b):
    o_rate_options = split_input(get_data(year=year, day=day, block=True), cast_int=False, split_blanks=False)
    c_rate_options = split_input(get_data(year=year, day=day, block=True), cast_int=False, split_blanks=False)
    o_rate = ''
    c_rate = ''
    o_rate_final = 0
    c_rate_final = 0

    for x in range(len(input_b[0])):
        o_zipped_digits = list(zip(*o_rate_options))
        c_zipped_digits = list(zip(*c_rate_options))

        if o_zipped_digits[x].count('0') > o_zipped_digits[x].count('1') and not o_rate_final:
            o_rate = o_rate + '0'
        else:
            o_rate = o_rate + '1'

        if c_zipped_digits[x].count('0') > c_zipped_digits[x].count('1') and not c_rate_final:
            c_rate = c_rate + '1'
        else:
            c_rate = c_rate + '0'

        # Search for remaining options
        o_rate_options = [o for o in o_rate_options if o.startswith(o_rate)]
        c_rate_options = [c for c in c_rate_options if c.startswith(c_rate)]
        print(o_rate_options, '\n', c_rate_options)

        if len(o_rate_options) == 1:
            o_rate_final = o_rate_options[0]
        if len(c_rate_options) == 1:
            c_rate_final = c_rate_options[0]

        if o_rate_final and c_rate_final:
            return int(o_rate_final,2) * int(c_rate_final,2)


if __name__ == '__main__':
    # Set puzzle of interest
    year = 2021
    day = 3

    # Get puzzle inputs
    puzzle = Puzzle(year=year, day=day)
    puzzle_input = split_input(get_data(year=year, day=day, block=True), cast_int=False, split_blanks=False)

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
