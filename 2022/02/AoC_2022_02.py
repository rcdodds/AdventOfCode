# Libraries
from aocd.models import Puzzle
from aocd import submit
import logging

logging.basicConfig(level=logging.WARNING)

OPTION_MAP_DICT = {
    "A": "Rock",
    "B": "Paper",
    "C": "Scissors",
    "X": "Rock",
    "Y": "Paper",
    "Z": "Scissors"
}

OPTION_CONFIG_DICT = {
    "Rock": {
        "score": 1,
        "beats": "Scissors",
        "loses_to": "Paper"
    },
    "Paper": {
        "score": 2,
        "beats": "Rock",
        "loses_to": "Scissors"
    },
    "Scissors": {
        "score": 3,
        "beats": "Paper",
        "loses_to": "Rock"
    }
}


def solve_part_a(part_a_input):
    score = 0
    for row_str in part_a_input.split("\n"):
        choices = row_str.split(" ")
        opp_choice = OPTION_MAP_DICT[choices[0]]
        my_choice = OPTION_MAP_DICT[choices[1]]

        # Add choice points
        score += OPTION_CONFIG_DICT[my_choice]["score"]

        # Add win/tie points
        if my_choice == opp_choice:
            score += 3
        elif OPTION_CONFIG_DICT[my_choice]["beats"] == opp_choice:
            score += 6

    return score


def solve_part_b(part_b_input):
    score = 0
    for row_str in part_b_input.split("\n"):
        choices = row_str.split(" ")
        opp_choice = OPTION_MAP_DICT[choices[0]]
        if choices[1] == "X":
            my_choice = OPTION_CONFIG_DICT[opp_choice]["beats"]
        elif choices[1] == "Z":
            my_choice = OPTION_CONFIG_DICT[opp_choice]["loses_to"]
        else:
            my_choice = opp_choice

        # Add choice points
        score += OPTION_CONFIG_DICT[my_choice]["score"]

        # Add win/tie points
        if my_choice == opp_choice:
            score += 3
        elif OPTION_CONFIG_DICT[my_choice]["beats"] == opp_choice:
            score += 6

    return score


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2022, 2)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a, 'solve_func': solve_part_a,
                      'answer': pzl.answer_a if pzl.answered_a else None},
                'B': {'solved': pzl.answered_b, 'solve_func': solve_part_b,
                      'answer': pzl.answer_b if pzl.answered_b else None}}

    # Test inputs
    test_data = 'A Y\nB X\nC Z'

    # Consider both puzzles
    for part in pzl_dict.keys():
        if pzl_dict[part]['solved'] and not backtest:
            print(f'Year {year} Day {day} Part {part} already solved with answer = {pzl_dict[part]["answer"]}')
        else:
            # Attempt solution
            pzl_dict[part]['answer'] = pzl_dict[part]['solve_func'](pzl.input_data if not use_test_data else test_data)
            print(f'Year {year} Day {day} Part {part} answer generated this run = {pzl_dict[part]["answer"]}')

            # Submit if ready
            if not use_test_data:
                submit(pzl_dict[part]['answer'], part=part, year=year, day=day)
