# Libraries
from aocd.models import Puzzle
from aocd import submit
import itertools

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

    return z


def find_solution(digit_direction):
    for input_number in itertools.product(digit_direction, repeat=7):
        z_result = 0
        input_counter = 0
        output_number = []

        for digit_number in range(14):
            if add_to_x[digit_number] > 0:
                in_digit = int(input_number[input_counter])
                input_counter += 1
            else:
                in_digit = (z_result % 26) + add_to_x[digit_number]

            if 1 <= in_digit <= 9:
                output_number.append(str(in_digit))
                z_result = solve_puzzle_piece(in_digit, digit_number, z_result)
            else:
                break

        if len(output_number) == 14:
            print(f'Actual number = {"".join(output_number)} >>>\t\tz = {z_result}')

        if not z_result and len(output_number) == 14:
            return ''.join(output_number)


if __name__ == '__main__':
    # Get & format puzzle data
    (year, day) = (2021, 24)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = [row.split(' ') for row in puzzle.input_data.split('\n')]

    # Solve a part of the puzzle
    if not puzzle.answered_a:
        submit(find_solution('987654321'), part='A', year=year, day=day)
    elif not puzzle.answered_b:
        submit(find_solution('123456789'), part='B', year=year, day=day)
    else:
        print(f'Puzzle for year {year} // day {day} already solved!\n'
              f'Answer for part A = {puzzle.answer_a}\n'
              f'Answer for part B = {puzzle.answer_b}')
