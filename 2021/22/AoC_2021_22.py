# Libraries
import re
import numpy as np
import itertools
from aocd.models import Puzzle
from aocd import submit


def solve_puzzle(pzl_data, letter):
    if letter == 'A':
        # Initialize board
        lower_bound = -50
        upper_bound = 50
        size = upper_bound - lower_bound + 1
        cube_array = np.zeros((size, size, size), dtype=np.int8)

        # Loop through each instruction
        instruction_regex = r'((?:on)|(?:off)) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)'
        for instruction_str in pzl_data.split('\n'):
            # Get important parts of input using regex
            instruction_components = re.match(instruction_regex, instruction_str).groups()

            # Set cubes on/off according to instructions
            if instruction_components[0] == 'on':
                cube_array[
                    int(instruction_components[1]) - lower_bound: int(instruction_components[2]) - lower_bound + 1,
                    int(instruction_components[3]) - lower_bound: int(instruction_components[4]) - lower_bound + 1,
                    int(instruction_components[5]) - lower_bound: int(instruction_components[6]) - lower_bound + 1
                ] = 1
            else:
                cube_array[
                    int(instruction_components[1]) - lower_bound: int(instruction_components[2]) - lower_bound + 1,
                    int(instruction_components[3]) - lower_bound: int(instruction_components[4]) - lower_bound + 1,
                    int(instruction_components[5]) - lower_bound: int(instruction_components[6]) - lower_bound + 1
                ] = 0

            print(f'{instruction_str} >>> {instruction_components} >>> {np.count_nonzero(cube_array)}')

        return np.count_nonzero(cube_array)

    elif letter == 'B':
        on_cubes = set()
        lower_bound = min(tuple(map(int, re.findall(r'-?\d+', pzl_data))))
        upper_bound = max(tuple(map(int, re.findall(r'-?\d+', pzl_data))))
        print(lower_bound, upper_bound, (upper_bound - lower_bound) ** 3)

        # # Loop through each instruction
        # instruction_regex = r'((?:on)|(?:off)) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)'
        # for instruction_str in pzl_data.split('\n'):
        #     # Get important parts of input using regex
        #     instruction_components = re.match(instruction_regex, instruction_str).groups()
        #
        #     # Find applicable cubes
        #     for cube in itertools.product(np.arange(int(instruction_components[1]),
        #                                             int(instruction_components[2]) + 1),
        #                                   np.arange(int(instruction_components[3]),
        #                                             int(instruction_components[4]) + 1),
        #                                   np.arange(int(instruction_components[5]),
        #                                             int(instruction_components[6]) + 1)):
        #
        #         # Apply rule
        #         if instruction_components[0] == 'on':
        #             on_cubes.add(cube)
        #         else:
        #             try:
        #                 on_cubes.remove(cube)
        #             except KeyError:
        #                 pass
        #
        # return len(on_cubes)
    else:
        raise Exception


if __name__ == '__main__':
    # Puzzle info
    testing = False
    ready_to_solve = True
    (year, day) = (2021, 22)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}

    # Test inputs
    test_data = 'on x=-20..26,y=-36..17,z=-47..7\non x=-20..33,y=-21..23,z=-26..28\non x=-22..28,y=-29..23,z=-38..16\non x=-46..7,y=-6..46,z=-50..-1\non x=-49..1,y=-3..46,z=-24..28\non x=2..47,y=-22..22,z=-23..27\non x=-27..23,y=-28..26,z=-21..29\non x=-39..5,y=-6..47,z=-3..44\non x=-30..21,y=-8..43,z=-13..34\non x=-22..26,y=-27..20,z=-29..19\noff x=-48..-32,y=26..41,z=-47..-37\non x=-12..35,y=6..50,z=-50..-2\noff x=-48..-32,y=-32..-16,z=-15..-5\non x=-18..26,y=-33..15,z=-7..46\noff x=-40..-22,y=-38..-28,z=23..41\non x=-16..35,y=-41..10,z=-47..6\noff x=-32..-23,y=11..30,z=-14..3\non x=-49..-5,y=-3..45,z=-29..18\noff x=18..30,y=-20..-8,z=-3..13\non x=-41..9,y=-7..43,z=-33..15\non x=-54112..-39298,y=-85059..-49293,z=-27449..7877\non x=967..23432,y=45373..81175,z=27513..53682'

    # Consider both puzzles
    for part in ['A', 'B']:
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(puzzle.input_data if not testing else test_data, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
