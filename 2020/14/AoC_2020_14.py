from aocd.models import Puzzle
from aocd import submit
import itertools


class InvalidPuzzleTypeError(Exception):
    """Raised when trying to work with a puzzle type that doesn't exist"""
    pass


def decimal_to_36bit(decimal_number):
    # String to hold result
    two_bit_string = ''

    # Loop through all possible bits
    for i in range(36):
        bit_worth = 2 ** (35 - i)
        # If this bit is needed, set it to 1
        if decimal_number >= bit_worth:
            two_bit_string = two_bit_string + '1'
            decimal_number -= bit_worth
        # Otherwise, set it to 0
        else:
            two_bit_string = two_bit_string + '0'

    return two_bit_string


def value_string_to_decimal(value_string):
    # Number to hold result
    number = 0

    # Loop through the bits
    for pos, bit in enumerate(value_string):
        # If this bit is set, add the value
        if bit == '1':
            number += (2 ** (len(value_string) - pos - 1))

    return number


def apply_mask(value, mask, do_nothing_char):
    # Loop through the strings
    for position, digit in enumerate(value):
        # If the mask has a relevant value in this position, overwrite that position of the input
        if mask[position] != do_nothing_char:
            value = value[:position] + mask[position] + value[position+1:]

    return value


def expand_floating(floating_address):
    addresses = []
    # Find number of floating digits to be substituted
    floating_bits = floating_address.count('X')

    # If there are no floating digits, just return the address
    if not floating_bits:
        addresses.append(floating_address)
    # Otherwise, return all possible variations
    else:
        # Create all options for the floating bits
        bit_replacements = [list(a) for a in itertools.product(['0', '1'], repeat=floating_bits)]
        # Create all concatenations
        for option in bit_replacements:
            new_address = floating_address
            for digit in option:
                new_address = new_address.replace('X', digit, 1)
            addresses.append(new_address)
    return addresses


def solve_puzzle(pzl_data, letter):
    # Dictionary of values in memory
    memory = {}

    if letter == 'A':
        current_mask = 'X' * 36     # Mask initially set to not overwrite anything
        # Loop through actions
        for action in pzl_data:
            # Update mask
            if action.startswith('mask'):
                current_mask = action.split(' ')[-1]
            # Write value to memory
            else:
                memory_address = int(action[action.find('[') + 1:action.find(']')])
                dec_num = int(action.split(' ')[-1])
                bit_str = decimal_to_36bit(dec_num)
                masked_bit_str = apply_mask(bit_str, current_mask, 'X')
                memory[memory_address] = masked_bit_str
        return sum([value_string_to_decimal(mem) for mem in memory.values()])

    elif letter == 'B':
        current_mask = '0' * 36     # Mask initially set to not overwrite anything
        # Loop through actions
        for action in pzl_data:
            # Update mask
            if action.startswith('mask'):
                current_mask = action.split(' ')[-1]
            # Write value to memory
            else:
                memory_address = int(action[action.find('[') + 1:action.find(']')])
                masked_addresses = expand_floating(apply_mask(decimal_to_36bit(memory_address), current_mask, '0'))
                dec_num = int(action.split(' ')[-1])
                for mem_add in masked_addresses:
                    memory[value_string_to_decimal(mem_add)] = dec_num
        return sum(memory.values())

    else:
        # Invalid letter submitted
        print('Gasp! You tried to use a puzzle type that does not exist.')
        raise InvalidPuzzleTypeError


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2020, 14)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    puzzle_data = puzzle_data.split('\n')

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
