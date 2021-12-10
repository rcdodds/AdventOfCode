from aocd.models import Puzzle
from aocd import get_data, submit
import pandas as pd
import numpy as np
import datetime
import json
import parse


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
    counts = []
    for entry in input_a:
        counts.append(len(set(list(entry.replace('\n', '')))))
    return sum(counts)


def puzzle_b(input_b):
    counts = []
    for entry in input_b:
        print(entry)
        common_answers = set(list(entry.replace('\n', '')))
        for person in entry.split('\n'):
            print(common_answers)
            common_answers = common_answers.intersection(set(list(person)))
        counts.append(len(common_answers))
        print(counts)
    return sum(counts)


if __name__ == '__main__':
    # Set puzzle of interest
    year = 2020
    day = 6

    # Get puzzle inputs
    puzzle = Puzzle(year=year, day=day)
    puzzle_input = split_input(get_data(year=year, day=day, block=True), cast_int=False, split_blanks=True)

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
