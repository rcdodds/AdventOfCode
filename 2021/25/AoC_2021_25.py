# Libraries
from aocd.models import Puzzle
from aocd import submit
import copy


class SeaFloor:
    def __init__(self, puzzle_input):
        self.board = [list(row_str) for row_str in puzzle_input.split('\n')]
        self.steps = 0

    def __repr__(self):
        return '\n'.join([''.join(row_string) for row_string in self.board])

    def simulate_round(self):
        # Initialize
        temp_board = copy.deepcopy(self.board)
        move_made = False

        # Loop through board (East-facing = row / col)
        for row_num in range(len(self.board)):
            skip = False
            for col_num in range(len(self.board[0])):
                # Skip this spot if a value has just been moved into it
                if skip:
                    skip = False    # Reset for next time
                    continue

                # East-facing logic
                if self.board[row_num][col_num] == '>':
                    # Move to next spot (if possible) while wrapping around (if necessary)
                    next_col = 0 if (col_num + 1) == len(self.board[0]) else (col_num + 1)
                    if self.board[row_num][next_col] == '.':
                        move_made = True                        # Set return flag
                        temp_board[row_num][col_num] = '.'      # Vacate current spot
                        temp_board[row_num][next_col] = '>'     # Move into next spot
                        skip = True     # Skip next spot to avoid pushing the same value more than once per step
        self.board = copy.deepcopy(temp_board)   # Store east-facing moves

        # Loop through board (South-facing = col / row)
        for col_num in range(len(self.board[0])):
            skip = False
            for row_num in range(len(self.board)):
                # Skip this spot if a value has just been moved into it
                if skip:
                    skip = False  # Reset for next time
                    continue

                # Move to next spot (if possible) while wrapping around (if necessary)
                if self.board[row_num][col_num] == 'v':
                    next_row = 0 if (row_num + 1) == len(self.board) else (row_num + 1)
                    if self.board[next_row][col_num] == '.':
                        move_made = True  # Set return flag
                        temp_board[row_num][col_num] = '.'  # Vacate current spot
                        temp_board[next_row][col_num] = 'v'  # Move into next spot
                        skip = True  # Skip next spot to avoid pushing the same value more than once per step
        self.board = copy.deepcopy(temp_board)      # Store south-facing moves
        self.steps += 1
        return move_made


def solve_puzzle_part_a(raw_pzl_input):
    sea_floor = SeaFloor(raw_pzl_input)
    while sea_floor.simulate_round():
        print(f'Still moving after {sea_floor.steps} steps')
    print(f'Stabilized after {sea_floor.steps} steps')
    return sea_floor.steps


if __name__ == '__main__':
    # Get & format puzzle data
    (year, day) = (2021, 25)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data

    # Solve a part of the puzzle
    if not puzzle.answered_a:
        submit(solve_puzzle_part_a(puzzle_data), part='A', year=year, day=day)
    else:
        print(f'Puzzle for year {year} // day {day} already solved!\n'
              f'Answer for part A = {puzzle.answer_a}\n'
              f'Answer for part B = {puzzle.answer_b}')
