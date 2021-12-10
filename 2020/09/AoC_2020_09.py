from aocd.models import Puzzle
from aocd import get_data, submit
import pandas as pd
import numpy as np
import datetime
import json
import parse
import re
import itertools


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
    for position in range(len(input_a)):
        if position > 24:
            # Get list to consider
            previous_numbers = input_a[position - 25:position]

            # Find all possible combinations
            all_combos = itertools.combinations(previous_numbers, 2)

            # Find all possible sums
            all_sums = [sum(x) for x in all_combos]

            # Determine if current number is NOT the sum of two recent numbers
            if not input_a[position] in all_sums:
                return input_a[position]


def puzzle_b(input_b):
    # Answers from part A
    answer_pos = 561
    answer_num = 70639851

    for start in range(0, answer_pos):
        contig_sum = 0
        while contig_sum <= answer_num:
            for current in range(start, answer_pos):
                contig_sum += input_b[current]
                # print(start, current, input_b[start:current+1])
                if contig_sum == answer_num:
                    return min(input_b[start:current+1]) + max(input_b[start:current+1])


if __name__ == '__main__':
    # Set puzzle of interest
    year = 2020
    day = 9

    # Get puzzle inputs
    puzzle = Puzzle(year=year, day=day)
    puzzle_input = split_input(get_data(year=year, day=day, block=True), cast_int=True, split_blanks=False)

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
