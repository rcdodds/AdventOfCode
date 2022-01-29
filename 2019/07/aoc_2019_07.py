# Libraries
import logging
import itertools
from aoc_util.intcode import IntcodeProgram
from aocd.models import Puzzle
from aocd import submit

logging.basicConfig(level=logging.WARNING)


def solve_part_a(part_a_input):
    thruster_results = set()
    for amp_tuple in itertools.permutations((0, 1, 2, 3, 4), r=5):
        amp_list, prior_output = list(amp_tuple), 0
        while amp_list:
            icp = IntcodeProgram(part_a_input, input_values=[amp_list.pop(0), prior_output])
            icp.run()
            prior_output = icp.get_diagnostic_code()
        thruster_results.add(prior_output)
    return max(thruster_results)


def solve_part_b(part_b_input):
    pass


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2019, 7)
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
