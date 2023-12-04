# Libraries
from aocd.models import Puzzle
from aocd import submit
import logging
import re

logging.basicConfig(level=logging.WARNING)


def solve_part_a(part_a_input, win_num_ct):
    score = 0
    for row in part_a_input.split("\n"):
        numbers = [int(x) for x in re.findall(r'\b(\d+)\b', row)[1:]]
        score += int(2 ** (len(set(numbers[:win_num_ct]) & set(numbers[win_num_ct:])) - 1))
    return score


def solve_part_b(part_b_input, win_num_ct):
    card_counts = [1 for r in part_b_input.split("\n")]
    for row_index, row_str in enumerate(part_b_input.split("\n")):
        numbers = [int(x) for x in re.findall(r'\b(\d+)\b', row_str)]
        cd_num = numbers[0]
        max_cd_num = cd_num + len(set(numbers[1:win_num_ct+1]) & set(numbers[win_num_ct+1:]))

        # Increment card score counts
        card_counts[cd_num:max_cd_num] = [current+card_counts[row_index] for current in card_counts[cd_num:max_cd_num]]
    return sum(card_counts)


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    winning_number_count = 5 if use_test_data else 10
    (year, day) = (2023, 4)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a, 'solve_func': solve_part_a,
                      'answer': pzl.answer_a if pzl.answered_a else None},
                'B': {'solved': pzl.answered_b, 'solve_func': solve_part_b,
                      'answer': pzl.answer_b if pzl.answered_b else None}}

    # Test inputs
    test_data = 'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\nCard 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\nCard 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\nCard 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\nCard 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\nCard 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'

    # Consider both puzzles
    for part in pzl_dict.keys():
        if pzl_dict[part]['solved'] and not backtest:
            print(f'Year {year} Day {day} Part {part} already solved with answer = {pzl_dict[part]["answer"]}')
        else:
            # Attempt solution
            pzl_dict[part]['answer'] = pzl_dict[part]['solve_func'](pzl.input_data if not use_test_data else test_data, winning_number_count)
            print(f'Year {year} Day {day} Part {part} answer generated this run = {pzl_dict[part]["answer"]}')

            # Submit if ready
            if not use_test_data:
                submit(pzl_dict[part]['answer'], part=part, year=year, day=day)
