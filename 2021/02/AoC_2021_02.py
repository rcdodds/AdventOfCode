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
    input_parts = input_row.split(' ')

    if input_parts[0] == 'up':
        return (0, -int(input_parts[1]))
    elif input_parts[0] == 'down':
        return (0, int(input_parts[1]))
    elif input_parts[0] == 'forward':
        return (int(input_parts[1]), 0)
    else:
        return (0,0)


def puzzle_a(input_a):
    (horizontal, depth) = (0, 0)
    for direction in input_a:
        (horizontal_delta, depth_delta) = divide_input_row(direction)
        (horizontal, depth) = (horizontal + horizontal_delta, depth + depth_delta)

    return horizontal * depth


def divide_input_row_b(input_row, current_aim):
    input_parts = input_row.split(' ')

    if input_parts[0] == 'up':
        return (0, 0, -int(input_parts[1]))
    elif input_parts[0] == 'down':
        return (0, 0, int(input_parts[1]))
    elif input_parts[0] == 'forward':
        return (int(input_parts[1]), current_aim * int(input_parts[1]), 0)
    else:
        return (0,0)


def puzzle_b(input_b):
    (horizontal, depth, aim) = (0, 0, 0)
    for direction in input_b:
        (horizontal_delta, depth_delta, aim_delta) = divide_input_row_b(direction, aim)
        (horizontal, depth, aim) = (horizontal + horizontal_delta, depth + depth_delta, aim + aim_delta)

    return horizontal * depth


if __name__ == '__main__':
    # Set puzzle of interest
    year = 2021
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
        print('Guess for puzzle A: ' + str(puzzle_a_result))
        print('Guess for puzzle B: ' + str(puzzle_b_result))

