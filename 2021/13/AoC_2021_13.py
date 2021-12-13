# Libraries
import numpy as np
from aocd.models import Puzzle
from aocd import submit


class PaperGrid:
    def __init__(self, points):
        # Add points
        self.coords = set()
        for p in points:
            self.coords.add(p)

        # Number of folds
        self.folds = 0

        # Original grid
        self.grid = self.show_paper()

    def fold(self, line_variable, line_value):
        # Consider all existing points
        new_coords = set()
        for pt in self.coords:
            # If on the "outside" of the line, need to change this portion of the coordinate
            if line_variable == 'x' and pt[0] > line_value:
                new_coords.add((line_value - (pt[0] - line_value), pt[1]))
            elif line_variable == 'y' and pt[1] > line_value:
                new_coords.add((pt[0], line_value - (pt[1] - line_value)))
            else:
                # Point is "inside" line and does not need to be changed
                new_coords.add((pt[0], pt[1]))

        # Overwrite self's property
        self.coords = new_coords
        self.folds += 1

    def visible_points(self):
        return len(self.coords)

    def find_shape(self):
        x_vals, y_vals = [], []
        for c in self.coords:
            x_vals.append(c[0])
            y_vals.append(c[1])

        return min(x_vals), max(x_vals), min(y_vals), max(y_vals)

    def show_paper(self):
        min_x, max_x, min_y, max_y = self.find_shape()

        self.grid = np.zeros((max_y+1, max_x+1)).astype(int)

        for p in self.coords:
            self.grid[p[1]][p[0]] = 1

        return self.grid


def solve_puzzle(coordinates, actions, letter):
    # Create object for future use
    TransparentPaper = PaperGrid(coordinates)

    if letter == 'A':
        # Perform one fold
        TransparentPaper.fold(actions[0][0], actions[0][1])
        return TransparentPaper.visible_points()

    elif letter == 'B':
        # Perform all folds
        for action in actions:
            TransparentPaper.fold(action[0], action[1])

        letter_grid = TransparentPaper.show_paper()
        print(letter_grid)
        return 0


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 13)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    puzzle_data = puzzle.input_data.split('\n\n')
    coords = []
    for row in puzzle_data[0].split('\n'):
        coords.append((int(row.split(',')[0]), int(row.split(',')[1])))
    instructions = []
    for r in puzzle_data[1].split('\n'):
        instructions.append((r.split(' ')[-1].split('=')[0], int(r.split(' ')[-1].split('=')[1])))

    # Consider both puzzles
    for part in ['A', 'B']:
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(coords, instructions, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
