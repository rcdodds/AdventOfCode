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


def create_map(input_strings):
    map_result = []
    for input_str in input_strings:
        input_row = input_str.replace('+', '').split(' ')
        map_result.append([input_row[0], int(input_row[1]), False])
    return map_result


def execute_code(codes):
    row = 0
    accumulator = 0
    infinite_loop = False

    while row in range(len(codes)):
        # If this row was already visited, don't execute
        if codes[row][2]:
            infinite_loop = True
            break
        else:
            # Mark row as visited
            codes[row][2] = True

            # Jump to new row
            if codes[row][0] == 'jmp':
                row += codes[row][1]
            else:
                # Add to accumulator
                if codes[row][0] == 'acc':
                    accumulator += codes[row][1]
                # Move to next row
                row += 1

    if not infinite_loop:
        return accumulator, True
    else:
        return accumulator, False


def puzzle_a(input_a):
    infinite_loop_value, infinite_loop_flag = execute_code(input_a)
    return infinite_loop_value


def puzzle_b(input_b):
    for action in range(len(input_b)):
        # Reset codes
        modified_input = create_map(split_input(get_data(year=year, day=day, block=True), cast_int=False, split_blanks=False))

        # Manipulate input
        if input_b[action][0] != 'acc':
            print('Attempting to modify action {} // {} // {}'.format(action, input_b[action], modified_input[action]))
            if input_b[action][0] == 'jmp':
                modified_input[action][0] = 'nop'
            elif input_b[action][0] == 'nop':
                modified_input[action][0] = 'jmp'

            # Attempt modified codes
            print('Attempting to modify action {} // {} // {}'.format(action, input_b[action], modified_input[action]))
            acc_val, success = execute_code(modified_input)

            # Done?
            if success:
                return acc_val


if __name__ == '__main__':
    # Set puzzle of interest
    year = 2020
    day = 8

    # Get puzzle inputs
    puzzle = Puzzle(year=year, day=day)
    puzzle_input = split_input(get_data(year=year, day=day, block=True), cast_int=False, split_blanks=False)

    # Solve puzzles
    puzzle_a_result = puzzle_a(create_map(puzzle_input))
    puzzle_b_result = puzzle_b(create_map(puzzle_input))

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
