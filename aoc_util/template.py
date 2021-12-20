# Libraries
from aocd.models import Puzzle
from aocd import submit


def solve_puzzle(pzl_data, letter):
    # Format puzzle input
    puzzle_data = pzl_data.split('\n')

    if letter == 'A':
        return 0

    elif letter == 'B':
        return 0


if __name__ == '__main__':
    # Puzzle info
    ready_to_solve = False
    (year, day) = (2021, 20)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}

    # Consider both puzzles
    for part in ['A', 'B']:
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(puzzle.input_data, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
