# Libraries
from aocd.models import Puzzle
from aocd import submit
import re
from copy import deepcopy


def calculate_score(winning_deck):
    winning_score = 0
    for i in range(1, len(winning_deck) + 1):
        winning_score += (winning_deck[-1 * i] * i)
    return winning_score


def standard_game(decks):
    while decks[0] and decks[1]:
        a_plays, b_plays = decks[0].pop(0), decks[1].pop(0)
        if a_plays > b_plays:
            decks[0].extend((a_plays, b_plays))
        else:
            decks[1].extend((b_plays, a_plays))
    return calculate_score(decks[0] if decks[0] else decks[1])


def recursive_game(decks, prior_decks=None):
    while decks[0] and decks[1]:
        if prior_decks is None:
            prior_decks = [deepcopy(decks)]   # First round of game - initialize list of prior decks
        elif decks in prior_decks:
            return True, calculate_score(decks[0])    # Prior state reached within this game - player A wins

        prior_decks.append(deepcopy(decks))   # Still playing - log new configuration
        a_plays, b_plays = decks[0].pop(0), decks[1].pop(0)     # Draw cards

        # Enough cards to recurse - start a new game to decide the winner of this round
        if len(decks[0]) >= a_plays and len(decks[1]) >= b_plays:
            new_decks = [decks[0][:a_plays], decks[1][:b_plays]]
            player_a_wins = recursive_game(new_decks)[0]
        # Not enough to recurse - higher card wins
        else:
            player_a_wins = True if a_plays > b_plays else False

        # Give the winner of this round the cards
        if player_a_wins:
            decks[0].extend((a_plays, b_plays))
        else:
            decks[1].extend((b_plays, a_plays))

    return True if decks[0] else False, calculate_score(decks[0] if decks[0] else decks[1])


def solve_puzzle_part(part_b_input, pzl_part):
    player_decks = [list(map(int, re.findall(r'\n(\d+)', x))) for x in part_b_input.split('\n\n')]
    if pzl_part == 'A':
        return standard_game(player_decks)
    else:
        return recursive_game(player_decks)[1]


if __name__ == '__main__':
    # Puzzle info
    test, solve, backtest = (False, True, False)
    (year, day) = (2020, 22)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a,
                      'answer': pzl.answer_a if pzl.answered_a else None,
                      'solve_func': solve_puzzle_part},
                'B': {'solved': pzl.answered_b,
                      'answer': pzl.answer_b if pzl.answered_b else None,
                      'solve_func': solve_puzzle_part}}

    # Test inputs
    test_data = 'Player 1:\n9\n2\n6\n3\n1\n\nPlayer 2:\n5\n8\n4\n7\n10'
    test_data = 'Player 1:\n43\n19\n\nPlayer 2:\n2\n29\n14'

    # Consider both puzzles
    for part in pzl_dict.keys():
        if pzl_dict[part]['solved'] and not backtest:
            print(f'Year {year} Day {day} Part {part} already solved with answer = {pzl_dict[part]["answer"]}')
        else:
            # Attempt solution
            pzl_dict[part]['answer'] = pzl_dict[part]['solve_func'](pzl.input_data if not test else test_data, part)
            print(f'Year {year} Day {day} Part {part} answer = {pzl_dict[part]["answer"]}')

            # Submit if ready
            if solve and pzl_dict[part]['answer']:
                submit(pzl_dict[part]['answer'], part=part, year=year, day=day)
