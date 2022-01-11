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
        # Remove invalid tickets
        valid_tickets = nearby_ticket_array[~np.any(valid_ticket_mask == 0, axis=1)]

        # Find all possible options for each column
        column_options = {}
        for col_num in range(len(valid_tickets[0])):
            col_vals = valid_tickets[:, col_num]
            col_opts = set()
            for field in field_dict.items():
                in_ranges = [cv for cv in col_vals if field[1]['range1'][0] <= cv <= field[1]['range1'][1] or
                                                        field[1]['range2'][0] <= cv <= field[1]['range2'][1]]
                out_ranges = [cv for cv in col_vals if cv not in in_ranges]
                if len(col_vals) == len(in_ranges):
                    col_opts.add(field[0])
            column_options[col_num] = col_opts
        
        # Reduce the possible mappings by considering everything uniquely identified
        while max(map(len, column_options.values())) > 1:
            for guessed in [g[1].copy().pop() for g in column_options.items() if len(g[1]) == 1]:
                for unknown in column_options.keys():
                    if guessed in column_options[unknown] and len(column_options[unknown]) > 1:
                        column_options[unknown].remove(guessed)

        # Replace sets with the definitive column headers
        for i in column_options.keys():
            column_options[i] = column_options[i].pop()

        result = 1
        for column_header in column_options.items():
            if column_header[1].find('departure') != -1:
                result *= my_ticket[column_header[0]]

        return result


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2020, 16)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    puzzle_data = puzzle.input_data.split('\n\n')
    # puzzle_data = 'class: 0-1 or 4-19\n' \
    #               'row: 0-5 or 8-19\n' \
    #               'seat: 0-13 or 16-19\n\n' \
    #               'your ticket:\n11,12,13\n\n' \
    #               'nearby tickets:\n' \
    #               '3,9,18\n' \
    #               '15,1,5\n' \
    #               '5,14,9'.split('\n\n')

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
