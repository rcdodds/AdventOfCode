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


def play_round_old(seat_list):
    new_seat_list = seat_list[:]

    # Loop through every row in the input
    for seat_row in range(len(seat_list)):
        # print('Checking row ' + str(seat_row+1))
        # Loop through every seat in each row
        for seat_col in range(len(seat_list[seat_row])):
            # print('Checking seat ' + str(seat_col+1))
            # Determine seat value
            seat_val = seat_list[seat_row][seat_col]

            # Skip floor
            if seat_val != '.':
                (left, right, up, down) = (max(0, seat_col-1), min(len(seat_list[seat_row]), seat_col+1),
                                           max(0, seat_row-1), min(len(seat_list), seat_row+1))
                adj_opposites = sum([row_str.count('#', left, right+1) for row_str in seat_list[up:down+1]])

                # Set opposite value to be searched for
                if seat_val == 'L':
                    # If there are 0 adjacent seats occupied, seat becomes occupied
                    if adj_opposites == 0:
                        new_seat_list[seat_row] = new_seat_list[seat_row][:seat_col] + '#' + \
                                                  new_seat_list[seat_row][seat_col + 1:]

                else:   # seat_val = '#'
                    adj_opposites -= 1  # The current seat will be found and must be subtracted

                    # If there are 4 or more adjacent seats occupied, seat becomes empty
                    if adj_opposites >= 4:
                        new_seat_list[seat_row] = new_seat_list[seat_row][:seat_col] + 'L' + \
                                                  new_seat_list[seat_row][seat_col + 1:]

    # Return new seat values
    return new_seat_list


def play_round(seat_list, reach, seats_to_fill, min_seats_to_leave):
    new_seat_list = seat_list[:]
    direction_vectors = [
        np.array([-1, 0]),    # Up
        np.array([1, 0]),     # Down
        np.array([0, -1]),    # Left
        np.array([0, 1]),     # Right
        np.array([-1, 1]),    # Up-Right
        np.array([1, 1]),     # Down-Right
        np.array([-1, -1]),   # Up-Left
        np.array([1, -1])    # Down-Left
    ]

    # Loop through every row in the input
    for seat_row in range(len(seat_list)):
        # print('Checking row ' + str(seat_row+1))
        # Loop through every seat in each row
        for seat_col in range(len(seat_list[seat_row])):
            # print('Checking seat ' + str(seat_col+1))
            # Determine seat value
            seat_val = seat_list[seat_row][seat_col]

            # Skip if current spot is actually floor
            if seat_val != '.':
                # Reset number of filled seats found to 0
                nearby_seats_filled = 0
                if seat_val == 'L':
                    threshold = seats_to_fill + 1
                else:   # seat_val = '#'
                    threshold = min_seats_to_leave

                # Consider each possible direction
                for vector in direction_vectors:
                    # Get ready to search
                    found_nonfloor_seat = False
                    scalar = 1
                    (row, col) = (seat_row, seat_col) + vector * scalar

                    # Check for occupied seats in the given direction
                    while (scalar <= reach) and not found_nonfloor_seat and row in range(len(seat_list)) and col in range(len(seat_list[seat_row])):
                        # Check result
                        if seat_list[row][col] != '.':
                            # Non-floor seat has been found - loop will break
                            found_nonfloor_seat = True

                            # Increment count if applicable
                            if seat_list[row][col] == '#':
                                nearby_seats_filled += 1
                        # Get ready for next iteration
                        else:
                            scalar += 1
                            (row, col) = (seat_row, seat_col) + vector * scalar

                    # Check if searching can be stopped early
                    if nearby_seats_filled >= threshold:
                        break

                # Take action if necessary
                if seat_val == 'L':
                    # If there are 0 adjacent seats occupied, seat becomes occupied
                    if nearby_seats_filled == seats_to_fill:
                        new_seat_list[seat_row] = new_seat_list[seat_row][:seat_col] + '#' + \
                                                  new_seat_list[seat_row][seat_col + 1:]

                else:   # seat_val = '#'
                    # If there are 4 or more adjacent seats occupied, seat becomes empty
                    if nearby_seats_filled >= min_seats_to_leave:
                        new_seat_list[seat_row] = new_seat_list[seat_row][:seat_col] + 'L' + \
                                                  new_seat_list[seat_row][seat_col + 1:]

    # Return new seat values
    print('\n'.join(new_seat_list))
    return new_seat_list


def solve_puzzle(pzl_data, letter):
    seat_history = {0: pzl_data}
    rounds_played = 0

    while True:
        # Set type of game via reach
        if letter == 'A':
            reach_range = 1
            min_to_fill = 0
            min_to_leave = 4
        elif letter == 'B':
            reach_range = 1000000
            min_to_fill = 0
            min_to_leave = 5
        else:
            # Invalid letter submitted
            print('Gasp! You tried to use a puzzle type that does not exist.')
            raise InvalidPuzzleTypeError

        # Play a round
        rounds_played += 1
        print('Playing round ' + str(rounds_played))
        seat_history[rounds_played] = play_round(seat_history[rounds_played - 1], reach_range, min_to_fill, min_to_leave)

        # Check whether or not steady-state has been reached
        if seat_history[rounds_played] == seat_history[rounds_played - 1]:
            break

    # After reaching steady state
    filled_seats = sum(row_string.count('#') for row_string in seat_history[rounds_played])
    return filled_seats


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2020, 11)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = False

    # puzzle_data = 'L.LL.LL.LL\nLLLLLLL.LL\nL.L.L..L..\nLLLL.LL.LL\nL.LL.LL.LL\nL.LLLLL.LL\n..L.L.....\nLLLLLLLLLL\nL.LLLLLL.L\nL.LLLLL.LL'

    # Format puzzle input
    delim = '\n'
    cast_int = False
    puzzle_data = puzzle_data.split('\n')
    if cast_int:
        puzzle_data = [int(num_str) for num_str in puzzle_data]

    # Consider both puzzles
    for part in ['A', 'B']:
        # If puzzle is not already solved...
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(puzzle_data, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
