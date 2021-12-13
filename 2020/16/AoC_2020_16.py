# Libraries
import re
import numpy as np
from aocd.models import Puzzle
from aocd import submit


def find_invalid_tickets(field_range_dict, ticket_array):
    # Assume everything is invalid by initializing a mask of 1s
    invalid_tickets = np.ones(ticket_array.shape)

    # Loop through all valid ranges for fields
    for field in field_range_dict.keys():
        for i in ['range1', 'range2']:
            # Range boundaries
            range_min = field_range_dict[field][i][0]
            range_max = field_range_dict[field][i][1]

            # If the ticket values are in a valid range, set the mask to 0
            invalid_tickets[np.logical_and(ticket_array >= range_min, ticket_array <= range_max)] = 0

    return invalid_tickets


def solve_puzzle(pzl_data, letter):
    # Split fields into list of tuples per fields
    field_name_regex = r'([a-z]*\s?[a-z]*): ([0-9]*)-([0-9]*) or ([0-9]*)-([0-9]*)\s?'
    field_dict = {}
    for match in re.findall(field_name_regex, pzl_data[0]):
        field_dict[match[0]] = {'range1': tuple(map(int, match[1:3])),
                                   'range2': tuple(map(int, match[3:5]))}

    # Split my ticket into list of ints
    my_ticket = [int(x) for x in pzl_data[1].split('\n')[-1].split(',')]

    # Split nearby tickets
    nearby_tickets = []
    for row in pzl_data[2].split('\n')[1:]:
        nearby_tickets.append([int(y) for y in row.split(',')])
    nearby_ticket_array = np.array(nearby_tickets)

    # Create mask of invalid ticket values
    invalid_ticket_mask = find_invalid_tickets(field_dict, nearby_ticket_array)
    valid_ticket_mask = np.invert(invalid_ticket_mask.astype(bool)).astype(int)

    if letter == 'A':
        return np.sum(nearby_ticket_array * invalid_ticket_mask).astype(int)

    elif letter == 'B':
        # Use first valid row of the ticket array for determining field order
        for i in range(valid_ticket_mask.shape[0]):
            if np.sum(valid_ticket_mask[i]) == len(valid_ticket_mask[i]):
                ticket = nearby_ticket_array[i]
                break


        return 0


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2020, 16)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    puzzle_data = puzzle.input_data.split('\n\n')

    # Consider both puzzles
    for part in ['A', 'B']:
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(puzzle_data, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
