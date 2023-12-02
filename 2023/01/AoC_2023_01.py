# Libraries
from aocd.models import Puzzle
from aocd import submit
import re
import logging

logging.basicConfig(level=logging.WARNING)

DIGIT_WORDS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def solve_part_a(part_a_input):
    calibration_sum = 0
    for row in part_a_input.split('\n'):
        digits = re.findall(r'\d', row)
        calibration_sum += int(digits[0]) * 10 + int(digits[-1])
    return calibration_sum


def solve_part_b(part_b_input):
    calibration_sum = 0
    for row in part_b_input.split('\n'):
        # Find first term
        search_terms = DIGIT_WORDS + [str(x + 1) for x in range(9)]
        search_results = [None if row.find(st) == -1 else row.find(st) for st in search_terms]
        first_term = search_terms[search_results.index(min(filter(lambda sr: sr is not None, search_results)))]
        tens_digit = int(first_term) if '0123456789'.find(first_term) >= 0 else DIGIT_WORDS.index(first_term) + 1

        # Find last term
        rvs_row = row[::-1]
        rvs_search_terms = [s[::-1] for s in search_terms]
        rvs_search_results = [None if rvs_row.find(st) == -1 else rvs_row.find(st) for st in rvs_search_terms]
        last_term = search_terms[rvs_search_results.index(min(filter(lambda sr: sr is not None, rvs_search_results)))]
        ones_digit = int(last_term) if '0123456789'.find(last_term) >= 0 else DIGIT_WORDS.index(last_term) + 1

        # Score
        calibration_sum += tens_digit * 10 + ones_digit
    return calibration_sum


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2023, 1)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a, 'solve_func': solve_part_a,
                      'answer': pzl.answer_a if pzl.answered_a else None},
                'B': {'solved': pzl.answered_b, 'solve_func': solve_part_b,
                      'answer': pzl.answer_b if pzl.answered_b else None}}

    # Test inputs
    # test_data = '1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet'
    # test_data = 'two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen'
    test_data = 'five\nthreefivethree\neightwo\nfiveeight3sppjtccnineeighteightnffgtlsdj \nthreethreetwothree'

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
