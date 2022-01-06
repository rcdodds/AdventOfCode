# Libraries
from aocd.models import Puzzle
from aocd import submit
import itertools
from functools import lru_cache

# Global variables from puzzle input
add_to_x = (15, 14, 11, -13, 14, 15, -7, 10, -12, 15, -16, -9, -8, -8)
divide_z = (1, 1, 1, 26, 1, 1, 26, 1, 26, 1, 26, 26, 26, 26)
add_to_y = (4, 16, 14, 3, 11, 13, 11, 7, 12, 15, 13, 1, 15, 4)


def solve_puzzle_piece(input_digit, digit_pos, prior_z):
    global add_to_x, divide_z, add_to_y

    w = input_digit
    x = (prior_z % 26) + add_to_x[digit_pos]
    x = int(x != w)                             # X is 1 if it is not equal to w, otherwise 0 (good)
    y = 25*x + 1                                # Either 1 or 26
    z = (prior_z // divide_z[digit_pos]) * y
    y = (w + add_to_y[digit_pos]) * x           # X is either 0 / 1
    z += y

    print(w, x, y, z)

    return z


def solve_puzzle_part_a(alu_instructions):
    # Loop through all possible 14-digit inputs (without 0 as digit) in decreasing order
    for input_number_str in itertools.product('987654321', repeat=14):
        # Initialize variables
        input_number = int(''.join(input_number_str))
        print(f'Validating {input_number}')
        input_digits = [int(dig) for dig in str(input_number)]
        result_z = 0

        # Loop through each input digit
        for pos, dig in enumerate(input_digits):
            result_z = solve_puzzle_piece(dig, pos, result_z)

        # If z is still 0 after validating all digits, this is a valid solution
        if result_z == 0:
            return input_number


        # # Loop through ALU applying each instruction
        # for instruction in alu_instructions:
        #     if instruction[0] == 'inp':
        #         variables[instruction[1]] = input_digits[input_digits_used]
        #         input_digits_used += 1
        #     elif instruction[0] == 'add':
        #         add_num = variables[instruction[2]] if instruction[2] in variables.keys() else int(instruction[2])
        #         variables[instruction[1]] += add_num
        #     elif instruction[0] == 'mul':
        #         mul_num = variables[instruction[2]] if instruction[2] in variables.keys() else int(instruction[2])
        #         variables[instruction[1]] += mul_num
        #     elif instruction[0] == 'div':
        #         div_num = variables[instruction[2]] if instruction[2] in variables.keys() else int(instruction[2])
        #         assert div_num != 0
        #         variables[instruction[1]] = variables[instruction[1]] // div_num
        #     elif instruction[0] == 'mod':
        #         mod_num = variables[instruction[2]] if instruction[2] in variables.keys() else int(instruction[2])
        #         assert variables[instruction[1]] >= 0
        #         assert mod_num > 0
        #         variables[instruction[1]] = variables[instruction[1]] % mod_num
        #     elif instruction[0] == 'eql':
        #         eql_num = variables[instruction[2]] if instruction[2] in variables.keys() else int(instruction[2])
        #         variables[instruction[1]] = int(variables[instruction[1]] == eql_num)
        # print(variables)
        #
        # # Store results if number is valid
        # if variables['z'] == 0:
        #     return input_number


def solve_puzzle_part_b(puzzle_data):
    print('part b')


if __name__ == '__main__':
    # Get & format puzzle data
    (year, day) = (2021, 24)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = [row.split(' ') for row in puzzle.input_data.split('\n')]

    # Solve a part of the puzzle
    if not puzzle.answered_a:
        submit(solve_puzzle_part_a(puzzle_data), part='A', year=year, day=day)
    elif not puzzle.answered_b:
        submit(solve_puzzle_part_b(puzzle_data), part='B', year=year, day=day)
    else:
        print(f'Puzzle for year {year} // day {day} already solved!\n'
              f'Answer for part A = {puzzle.answer_a}\n'
              f'Answer for part B = {puzzle.answer_b}')
