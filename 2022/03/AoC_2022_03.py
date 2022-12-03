# Libraries
from aocd.models import Puzzle
from aocd import submit
import logging

logging.basicConfig(level=logging.WARNING)


def score_char(ch):
    unicode_val = ord(ch)
    if unicode_val >= 97:
        return unicode_val - 96
    else:
        return unicode_val - 38


def solve_part_a(part_a_input):
    score = 0
    for rucksack_str in part_a_input.split("\n"):
        divider_index = int(len(rucksack_str) / 2)
        common = ''.join(set(rucksack_str[:divider_index]).intersection(set(rucksack_str[divider_index:])))
        assert len(common) == 1
        score += score_char(common)
    return score


def solve_part_b(part_b_input):
    score = 0
    current_index = 0
    group_size = 3
    groups = part_b_input.split("\n")
    while current_index < len(groups):
        common = ''.join(set(groups[current_index]).intersection(set(groups[current_index+1])).intersection(set(groups[current_index+2])))
        score += score_char(common)
        current_index += 3
    return score


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2022, 3)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a, 'solve_func': solve_part_a,
                      'answer': pzl.answer_a if pzl.answered_a else None},
                'B': {'solved': pzl.answered_b, 'solve_func': solve_part_b,
                      'answer': pzl.answer_b if pzl.answered_b else None}}

    # Test inputs
    test_data = ''

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
