# Libraries
from aocd.models import Puzzle
from aocd import submit


class Scanner:
    def __init__(self, number, beacons):
        self.number = number
        self.beacons = beacons

    def __repr__(self):
        return f'Scanner #{self.number} = {self.beacons}'

    def rotate(self):
        rotations = []


def solve_puzzle_part_a(puzzle_data):
    # Instantiate each scanner
    for i, beacon_list in enumerate(puzzle_data):
        s = Scanner(i, beacon_list)
        print(repr(s))

    return None


def solve_puzzle_part_b(puzzle_data):
    return None


if __name__ == '__main__':
    # Get & format puzzle data
    (year, day) = (2021, 19)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data

    scanners_list = []
    for scanner_str in puzzle_data.split('\n\n'):
        scanner_list = []
        for beacon_str in scanner_str.split('\n'):
            if 'scanner' not in beacon_str:
                scanner_list.append(list(map(int, beacon_str.split(','))))
        scanners_list.append(scanner_list)

    # Solve a part of the puzzle
    if not puzzle.answered_a:
        submit(solve_puzzle_part_a(scanners_list), part='A', year=year, day=day)
    elif not puzzle.answered_b:
        submit(solve_puzzle_part_b(scanners_list), part='B', year=year, day=day)
    else:
        print(f'Puzzle for year {year} // day {day} already solved!\n'
              f'Answer for part A = {puzzle.answer_a}\n'
              f'Answer for part B = {puzzle.answer_b}')
