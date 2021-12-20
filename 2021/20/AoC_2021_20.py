# Libraries
import numpy as np
from aocd.models import Puzzle
from aocd import submit


def get_slice(array2d, pos_i, pos_j, radius, border_val):
    # Adjust coordinate math to incorporate padding
    pad_size = radius
    pos_i += pad_size
    pos_j += pad_size

    # Add padding
    array2d = np.pad(array2d, pad_width=pad_size, mode='constant', constant_values=border_val)

    # Get slice
    sliced_array = array2d[pos_i - radius:pos_i + radius + 1, pos_j - radius:pos_j + radius + 1]

    # Return as concatenated string
    return ''.join(''.join(x) for x in sliced_array)


def enhance_image(start_image, enhancement_algorithm, b_val):
    enhanced_image = np.full(start_image.shape, '.', dtype=str)

    for i in range(start_image.shape[0]):
        for j in range(start_image.shape[1]):
            # Get the 9 digits from the input image
            output_chars = get_slice(start_image, i, j, 1, b_val)

            # Find the number in binary
            output_index = int(''.join(['0' if ch == '.' else '1' for ch in output_chars]), 2)

            # Set the output image
            enhanced_image[i, j] = enhancement_algorithm[output_index]

    return enhanced_image


def solve_puzzle(pzl_data, letter):
    # Format puzzle input
    puzzle_data = pzl_data.split('\n\n')
    algorithm = puzzle_data[0]
    image = np.array([list(r) for r in puzzle_data[1].split('\n')])

    if letter == 'A':
        rounds = 2

    elif letter == 'B':
        rounds = 50

    border_value = '.'
    for r in range(rounds):
        # Add a border to the image
        image = np.pad(image, pad_width=1, mode='constant', constant_values=border_value)

        # Enhance the image
        print(f'Enhancement round {r+1} of {rounds}')
        image = enhance_image(image, algorithm, border_value)

        # Find what the new border needs to be
        border_value = algorithm[int(''.join(['0' if ch == '.' else '1' for ch in border_value*9]), 2)]

    return np.count_nonzero(image == '#')


if __name__ == '__main__':
    # Puzzle info
    ready_to_solve = True
    (year, day) = (2021, 20)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}

    # Test input
    # puzzle_data = '..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#\n\n#..#.\n#....\n##..#\n..#..\n..###'

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

            # Only submit one part at a time
            break
