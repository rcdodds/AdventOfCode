# Standard functionality
from functools import lru_cache
import re
import itertools
import datetime
import json

# Additional libraries
import pandas as pd
import numpy as np

# Advent of Code libraries
from aocd.models import Puzzle
from aocd import submit


class InvalidPuzzleTypeError(Exception):
    """Raised when trying to work with a puzzle type that doesn't exist"""
    pass


def check_board(board_list, called_numbers):
    win = False     # Default win to False
    winning_numbers = [0,0,0,0,0]
    col_data = {}

    # Check for win by rows
    for r, row in enumerate(board_list):
        # If all numbers in a row have been called, this board has won
        if len(set(row).intersection(called_numbers)) == len(row):
            win = True
            winning_numbers = row

    # Check for win by columns
    for col_num in range(len(board_list[0])):
        col_data[col_num] = []
        for row_num in range(len(board_list)):
            col_data[col_num].append(board_list[row_num][col_num])

    for col in list(col_data.values()):
        # If all numbers in a row have been called, this board has won
        if len(set(col).intersection(called_numbers)) == len(col):
            win = True
            winning_numbers = col

    return win, winning_numbers


def solve_puzzle(bingo_calls, bingo_boards, letter):

    if letter in ['A', 'B']:
        for num_called, call in enumerate(bingo_calls):
            for board in bingo_boards:
                board_wins, board_winning_numbers = check_board(board, bingo_calls[:num_called+1])
                if board_wins:
                    # Calculate score
                    all_nums_on_board = set()
                    for row in board:
                        for value in row:
                            all_nums_on_board.add(value)
                    numbers_not_called = all_nums_on_board - set(bingo_calls[:num_called+1])
                    score = sum(numbers_not_called) * call

                    if letter == 'A':
                        return score
                    elif letter == 'B':
                        if len(bingo_boards) > 1:
                            bingo_boards.remove(board)
                        else:
                            return score

    else:
        # Invalid letter submitted
        print('Gasp! You tried to use a puzzle type that does not exist: ' + str(letter))
        raise InvalidPuzzleTypeError


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 4)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': False, 'guess': 0}, 'B': {'solved': False, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    delim = '\n'
    cast_int = False
    puzzle_data = puzzle_data.split('\n\n')
    if cast_int:
        puzzle_data = [int(num_str) for num_str in puzzle_data]

    # Make calls / boards
    calls = [int(y) for y in puzzle_data[0].split(',')]
    boards = []
    for brd_data in puzzle_data[1:]:
        bingo_brd = []
        for row_data in brd_data.split('\n'):
            bingo_brd.append([int(x) for x in re.split(' +', row_data) if x != ''])
        boards.append(bingo_brd)

    # Consider both puzzles
    for part in ['A', 'B']:
        # If puzzle is not already solved...
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(calls, boards, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
