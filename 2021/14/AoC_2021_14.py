# Libraries
import re
from aocd.models import Puzzle
from aocd import submit


class Polymer:
    def __init__(self, p_template, rules):
        # Dictionary of rules
        self.rules = rules

        # Initialize dictionary of counts for existing 2-character strings
        self.pair_counts = {two_char_str: p_template.count(two_char_str)
                            for two_char_str in set(re.findall(r'(?=([A-Z][A-Z]))', p_template))}

        # Initialize dictionary of counts for single letters
        self.char_counts = {ch: p_template.count(ch) for ch in set(p_template)}

    def apply_rules(self):
        # Pull existing strings into new dictionary so whole round can be played at once
        new_counts = {}

        # Loop through all existing 2-character substrings that must change because of rules
        for str_to_change in set(self.pair_counts.keys()).intersection(set(self.rules.keys())):

            # The 2 existing characters will be now separated by the value from the corresponding rule
            new_char = self.rules[str_to_change]
            for new_str in [str_to_change[0] + new_char, new_char + str_to_change[1]]:
                try:
                    new_counts[new_str] += self.pair_counts[str_to_change]
                except KeyError:
                    new_counts[new_str] = self.pair_counts[str_to_change]

            # Increment count of character added
            try:
                self.char_counts[new_char] += self.pair_counts[str_to_change]
            except KeyError:
                self.char_counts[new_char] = self.pair_counts[str_to_change]

        # Any existing 2-character substring that is NOT in the rules will remain untouched
        for not_to_change in set(self.pair_counts.keys()) - set(self.rules.keys()):
            try:
                new_counts[not_to_change] += self.pair_counts[not_to_change]
            except KeyError:
                new_counts[not_to_change] = self.pair_counts[not_to_change]

        # Store counts
        self.pair_counts = new_counts


def solve_puzzle(poly_temp, rules_dict, letter):
    poly = Polymer(poly_temp, rules_dict)

    if letter == 'A':
        rounds = 10
    elif letter == 'B':
        rounds = 40

    for step in range(rounds):
        poly.apply_rules()

    return max(poly.char_counts.values()) - min(poly.char_counts.values())


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 14)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    puzzle_data = puzzle.input_data.split('\n\n')
    polymer_template = puzzle_data[0]
    pair_insertion_rules = {}
    for rule in puzzle_data[1].split('\n'):
        pair_insertion_rules[rule.split(' -> ')[0]] = rule.split(' -> ')[1]

    # Consider both puzzles
    for part in ['A', 'B']:
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(polymer_template, pair_insertion_rules, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
