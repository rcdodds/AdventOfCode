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


def puzzle_a(input_a, row_inc, col_inc, max_row, max_col):
    trees_hit = 0
    row = 0
    col = 0
    while row < max_row:
        if input_a[row][col % max_col] == '#':
            trees_hit += 1
        row += row_inc
        col += col_inc
    return trees_hit


def puzzle_b(input_b, result_a):
    result_b = result_a
    for (row_add, col_add) in [(1, 1), (1, 5), (1, 7), (2, 1)]:
        trees = puzzle_a(input_b, row_add, col_add, len(input_b), len(input_b[0]))
        result_b = result_b * trees
    return result_b


if __name__ == '__main__':
    # Set puzzle of interest
    year = 2020
    day = 3

    # Get puzzle inputs
    puzzle = Puzzle(year=year, day=day)
    puzzle_input = split_input(get_data(year=year, day=day, block=True), cast_int=False)

    # Solve puzzles
    puzzle_a_result = puzzle_a(puzzle_input, 1, 3, len(puzzle_input), len(puzzle_input[0]))
    puzzle_b_result = puzzle_b(puzzle_input, puzzle_a_result)

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
        print('Solution for puzzle A: ' + str(puzzle_a_result))
        print('Solution for puzzle B: ' + str(puzzle_b_result))

