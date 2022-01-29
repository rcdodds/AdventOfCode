# Libraries
import logging
import re
import numpy as np
from aocd.models import Puzzle
from aocd import submit

logging.basicConfig(level=logging.WARNING)


def check_repeated_digits(input_number):
    return bool(re.search(r'(\d)\1', str(input_number)))


def check_all_digits_increase(input_number):
    return np.all(np.diff(list(map(int, list(str(input_number))))) >= 0)


def check_digit_repeats_twice(input_number):
    repetitions = re.finditer(r'(\d)\1+', str(input_number))
    return bool(2 in (len(r.group()) for r in repetitions))


def solve_part_a():
    return sum([bool(check_repeated_digits(x) and check_all_digits_increase(x)) for x in range(264360, 746326, 1)])


def solve_part_b():
    return sum([bool(check_digit_repeats_twice(x) and check_all_digits_increase(x)) for x in range(264360, 746326, 1)])


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, False)
    (year, day) = (2019, 4)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a, 'solve_func': solve_part_a,
                      'answer': pzl.answer_a if pzl.answered_a else None},
                'B': {'solved': pzl.answered_b, 'solve_func': solve_part_b,
                      'answer': pzl.answer_b if pzl.answered_b else None}}

    # Consider both puzzles
    for part in pzl_dict.keys():
        if pzl_dict[part]['solved'] and not backtest:
            print(f'Year {year} Day {day} Part {part} already solved with answer = {pzl_dict[part]["answer"]}')
        else:
            # Attempt solution
            pzl_dict[part]['answer'] = pzl_dict[part]['solve_func']()
            print(f'Year {year} Day {day} Part {part} answer generated this run = {pzl_dict[part]["answer"]}')

            # Submit if ready
            if not use_test_data:
                submit(pzl_dict[part]['answer'], part=part, year=year, day=day)
