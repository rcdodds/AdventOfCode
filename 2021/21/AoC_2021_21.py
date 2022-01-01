# Libraries
import re
import numpy as np
from aocd.models import Puzzle
from aocd import submit
from copy import deepcopy
import operator
import itertools
from functools import wraps, lru_cache


def hash_dict(solve_quantum_puzzle):
    """Transform mutable dictionary into immutable to be compatible with cache"""
    class NestedDict(dict):
        def __hash__(self):
            return hash(frozenset(frozenset(self[key].items()) for key in self.keys()))

    @wraps(solve_quantum_puzzle)
    def wrapped(*args, **kwargs):
        args = tuple([NestedDict(arg) if isinstance(arg, dict) else arg for arg in args])
        kwargs = {k: NestedDict(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
        return solve_quantum_puzzle(*args, **kwargs)
    return wrapped


@hash_dict
@lru_cache(maxsize=None)
def solve_quantum_puzzle(current_game_dict, rolls_now):
    wins = (0, 0)
    for die_roll in map(sum, [x for x in itertools.product([1, 2, 3], repeat=3)]):
        new_game_dict = deepcopy(current_game_dict)
        new_game_dict['positions'][rolls_now] = (new_game_dict['positions'][rolls_now] + die_roll - 1) % 10 + 1
        new_game_dict['scores'][rolls_now] += new_game_dict['positions'][rolls_now]
        rolls_next = rolls_now % len(new_game_dict['positions'].keys()) + 1

        if new_game_dict['scores'][rolls_now] >= 21:
            if rolls_now == 1:
                wins = tuple(map(operator.add, wins, tuple((1, 0))))
            else:
                wins = tuple(map(operator.add, wins, tuple((0, 1))))
        else:
            wins = tuple(map(operator.add, wins, solve_quantum_puzzle(new_game_dict, rolls_next)))
    return wins

# Initialize deterministic game
dice_rolls = 0
last_roll = 0
next_player = 1


def roll_die():
    # Use globals
    global dice_rolls, last_roll

    # Get the roll values
    rolls = ((np.array([1, 2, 3]) + last_roll - 1) % 100) + 1

    # Update global tracking variables
    dice_rolls += 3
    last_roll = rolls[-1]

    # Move player
    return np.sum(rolls)


def solve_puzzle(pzl_data, letter):
    # Use globals
    global dice_rolls, next_player

    # Format puzzle input
    game_info = {'positions': {}, 'scores': {}}
    for player in re.findall(r'Player ([0-9]+) starting position: ([2-9]|(?:10))', pzl_data):
        game_info['positions'][int(player[0])] = int(player[1])
        game_info['scores'][int(player[0])] = 0
    print(game_info)

    if letter == 'A':
        # Play round
        while max(game_info['scores'].values()) < 1000:
            game_info['positions'][next_player] = (game_info['positions'][next_player] + roll_die() - 1) % 10 + 1
            game_info['scores'][next_player] += game_info['positions'][next_player]
            next_player = next_player % len(game_info['positions'].keys()) + 1
        return min(game_info['scores'].values()) * dice_rolls

    elif letter == 'B':
        universe_counts = solve_quantum_puzzle(game_info, 1)
        print(universe_counts)
        return max(universe_counts)


if __name__ == '__main__':
    # Puzzle info
    testing = False
    ready_to_solve = True
    (year, day) = (2021, 21)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}

    # Test inputs
    test_data = 'Player 1 starting position: 4\nPlayer 2 starting position: 8'

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
