from aocd.models import Puzzle
from aocd import get_data, submit
import pandas as pd
import numpy as np
import datetime
import json
import parse


def split_input(input_str, cast_int):
    if cast_int:
        return [int(s) for s in input_str.split('\n')]
    else:
        return input_str.split('\n')


def divide_input_row(input_row):
    dash_pos = input_row.find('-')
    space_pos = input_row.find(' ')
    colon_pos = input_row.find(':')

    minimum = int(input_row[:dash_pos])
    maximum = int(input_row[dash_pos + 1:space_pos])
    character = input_row[space_pos + 1:colon_pos]
    password = input_row[colon_pos + 2:]

    # print('{} >>> min={}, max={}, char={}, pass={}'.format(input_row, minimum, maximum, character, password))
    return minimum, maximum, character, password


def puzzle_a(input_a):
    valid_passwords = 0
    for input_password in input_a:
        mn, mx, chr, pwd = divide_input_row(input_password)

        if pwd.count(chr) in range(mn, mx+1):
            valid_passwords += 1
    return valid_passwords


def puzzle_b(input_b):
    valid_passwords = 0
    for input_password in input_b:
        low, high, letter, passwd = divide_input_row(input_password)

        if (passwd[low - 1] == letter) + (passwd[high - 1] == letter) == 1:
            valid_passwords += 1
    return valid_passwords


if __name__ == '__main__':
    # Set puzzle of interest
    year = 2020
    day = 2

    # Get puzzle inputs
    puzzle = Puzzle(year=year, day=day)
    puzzle_input = split_input(get_data(year=year, day=day, block=True), cast_int=False)

    # Solve puzzles
    puzzle_a_result = puzzle_a(puzzle_input)
    puzzle_b_result = puzzle_b(puzzle_input)

    ready = True
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
    else:
        print('Solution for puzzle A: {}'.format(puzzle_a_result))
        print('Solution for puzzle B: {}'.format(puzzle_b_result))

