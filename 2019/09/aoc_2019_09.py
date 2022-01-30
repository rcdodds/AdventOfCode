# Libraries
import logging
from aocd.models import Puzzle
from aocd import submit
from aoc_util.intcode import IntcodeProgram

logging.basicConfig(level=logging.WARNING)


def solve_part_a(part_a_input):
    icp = IntcodeProgram(part_a_input, input_values=1)
    icp.run()
    return icp.get_diagnostic_code()


def solve_part_b(part_b_input):
    icp = IntcodeProgram(part_b_input, input_values=2)
    icp.run()
    return icp.get_diagnostic_code()


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2019, 9)
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
