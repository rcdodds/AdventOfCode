# Libraries
from aocd.models import Puzzle
from aocd import submit


def solve_puzzle_part_a(puzzle_data):
    return 0


def solve_puzzle_part_b(puzzle_data):
    return 0


if __name__ == '__main__':
    # Get & format puzzle data
    (year, day) = (2021, 1)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data.split('\n')

    # Solve a part of the puzzle
    if not puzzle.answered_a:
        submit(solve_puzzle_part_a(puzzle_data), part='A', year=year, day=day)
    elif not puzzle.answered_b:
        submit(solve_puzzle_part_b(puzzle_data), part='B', year=year, day=day)
    else:
        print(f'Puzzle for year {year} // day {day} already solved!\n'
              f'Answer for part A = {puzzle.answer_a}\n'
              f'Answer for part B = {puzzle.answer_b}')
