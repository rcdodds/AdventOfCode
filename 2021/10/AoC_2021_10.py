# Common libraries
from collections import deque
import numpy as np

# Advent of Code libraries
from aocd.models import Puzzle
from aocd import submit

# Global variables
open_chars = ['(', '[', '{', '<']
close_chars = [')', ']', '}', '>']


class InvalidPuzzleTypeError(Exception):
    """Raised when trying to work with a puzzle type that doesn't exist"""
    def __init__(self, attempted):
        pass


class SyntaxLine:
    def __init__(self, syntax_code_line_str):
        self.value = syntax_code_line_str

        # Assume line is perfect
        self.corrupted = False
        self.incomplete = False
        self.corr_char = ''
        self.close_seq = ''
        self.close_seq_score = 0

        # Parse line for errors
        self.check_issues()

    def check_issues(self):
        # Stack for open chunk characters
        open_chunks = deque()

        # Loop through line of code
        for char in self.value:
            # Open a new chunk
            if char in open_chars:
                open_chunks.append(char)
            # The active chunk has been closed properly
            elif close_chars.index(char) == open_chars.index(open_chunks[-1]):
                open_chunks.pop()
            # A close character has been encountered that does not match the recent open char. This line is corrupted.
            else:
                self.corrupted = True
                self.corr_char = char
                break

        # End of line has been reached without any corruption issues.
        if not self.corrupted:
            # Construct missing closing sequence
            while open_chunks:
                self.close_seq = self.close_seq + close_chars[open_chars.index(open_chunks.pop())]

            # Set other incompletion properties
            if self.close_seq:
                self.incomplete = True
                self.score_seq()

    def score_seq(self):
        for close in self.close_seq:
            self.close_seq_score = self.close_seq_score * 5 + close_chars.index(close) + 1


def solve_puzzle(pzl_data, letter):
    corrupted_chars = {}
    closing_sequences = {}

    # Loop through each row, adding errors to appropriate dictionary
    for i, val in enumerate(pzl_data):
        # Create instance of class
        line = SyntaxLine(val)

        # If line is corrupted, store corrupted character
        if line.corrupted:
            corrupted_chars[i] = line.corr_char

        # If line is incomplete, store missing closing sequence
        if line.incomplete:
            closing_sequences[i] = line.close_seq_score

    if letter == 'A':
        corrupted_counts = [list(corrupted_chars.values()).count(c) for c in close_chars]
        return int(sum(np.array(corrupted_counts) * np.array([3, 57, 1197, 25137])))

    elif letter == 'B':
        return int(np.median(np.array(list(closing_sequences.values()))))

    else:
        raise InvalidPuzzleTypeError(letter)


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 10)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    # puzzle_data = '[({(<(())[]>[[{[]{<()<>>\n[(()[<>])]({[<{<<[]>>(\n{([(<{}[<>[]}>{[]{[(<()>\n(((({<>}<{<{<>}{[]{[]{}\n[[<[([]))<([[{}[[()]]]\n[{[{({}]{}}([{[{{{}}([]\n{<[[]]>}<{[{[{[]{()[[[]\n[<(<(<(<{}))><([]([]()\n<{([([[(<>()){}]>(<<{{\n<{([{{}}[<[[[<>{}]]]>[]]'
    puzzle_data = puzzle_data.split('\n')
    # puzzle_data = [int(puzzle_string) for puzzle_string in puzzle_data]

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
