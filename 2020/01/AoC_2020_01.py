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


def puzzle_a(input_a):
    for i in input_a:
        for j in input_a:
            if i + j == 2020 and i <= j:
                print('(A) - i={i} // j={j} // i+j={sum} // i*j={product}'.format(i=i, j=j, sum=i + j, product=i * j))
                return i * j


def puzzle_b(input_b):
    possible_solutions = set()
    for i in input_b:
        for j in input_b:
            for k in input_b:
                if i + j + k == 2020 and (i, j, k) not in possible_solutions:
                    print('i={i} // j={j} // k={k} // i+j+k={sum} // i*j*k={product}'
                          .format(i=i, j=j, k=k, sum=i + j + k, product=i * j * k))
                    return i * j * k


if __name__ == '__main__':
    # Set puzzle of interest
    year = 2020
    day = 1

    # Get puzzle inputs
    puzzle = Puzzle(year=year, day=day)
    puzzle_input = split_input(get_data(year=year, day=day, block=True), cast_int=True)

    # Solve puzzles
    puzzle_a_result = puzzle_a(puzzle_input)
    puzzle_b_result = puzzle_b(puzzle_input)

    ready = False
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
        print('Guess for puzzle A: ' + str(puzzle_a_result))
        print('Guess for puzzle B: ' + str(puzzle_b_result))

