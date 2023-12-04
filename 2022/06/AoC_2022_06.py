# Libraries
from aocd.models import Puzzle
from aocd import submit
import logging

logging.basicConfig(level=logging.WARNING)


def find_marker(input_str, message_size):
    for ch in range(len(input_str) - message_size):
        ch_index = ch + message_size
        if len(set(input_str[ch_index - message_size: ch_index])) == message_size:
            return ch_index


def solve_part_a(part_a_input):
    return find_marker(part_a_input, 4)


def solve_part_b(part_b_input):
    return find_marker(part_b_input, 14)


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2022, 6)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a, 'solve_func': solve_part_a,
                      'answer': pzl.answer_a if pzl.answered_a else None},
                'B': {'solved': pzl.answered_b, 'solve_func': solve_part_b,
                      'answer': pzl.answer_b if pzl.answered_b else None}}

    # Test inputs
    test_data = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'

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
