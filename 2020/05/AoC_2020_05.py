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


def find_seat(seat_string):
    # Reset boundaries
    min_row = 0
    max_row = 127
    min_col = 0
    max_col = 7

    # Find row number
    for row_char in seat_string[:7]:
        if row_char == 'B':
            min_row += int((len(range(min_row, max_row + 1))) / 2)
        elif row_char == 'F':
            max_row -= int((len(range(min_row, max_row + 1))) / 2)
        else:
            print('ERROR')

    # Find column number
    for col_char in seat_string[7:]:
        if col_char == 'R':
            min_col += int((len(range(min_col, max_col + 1))) / 2)
        elif col_char == 'L':
            max_col -= int((len(range(min_col, max_col + 1))) / 2)
        else:
            print('ERROR')

    # Confirm single seat identified
    if min_row == max_row and min_col == max_col:
        return min_row, min_col
    else:
        print('ERROR')


def puzzle_a(input_a):
    seatIDs = []
    # Find a new seat ID
    for entry in input_a:
        row, col = find_seat(entry)
        seatIDs.append(row * 8 + col)
    return max(seatIDs)


def puzzle_b(input_b):
    all_seats = {}
    for i in range(128):
        all_seats[i] = [j for j in range(8)]

    for entry in input_b:
        row, col = find_seat(entry)
        all_seats[row].remove(col)

    my_seat_id = 0
    for row_entry in list(all_seats.keys()):
        if len(all_seats[row_entry]) == 1:
            col_entry = all_seats[row_entry][0]
            my_seat_id = row_entry * 8 + col_entry

    return my_seat_id


if __name__ == '__main__':
    # Set puzzle of interest
    year = 2020
    day = 5

    # Get puzzle inputs
    puzzle = Puzzle(year=year, day=day)
    puzzle_input = split_input(get_data(year=year, day=day, block=True), cast_int=False)

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
