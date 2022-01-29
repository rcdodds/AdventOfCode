# Libraries
from aocd.models import Puzzle
from aocd import submit
import logging
from aoc_util.intcode import IntcodeProgram

logging.basicConfig(level=logging.WARNING)


def solve_part_a(part_a_input):
    # Structure input
    ip_input = part_a_input.split(',')
    ip_input[1] = 12
    ip_input[2] = 2

    # Run program
    ip = IntcodeProgram(ip_input)
    ip.run()
    return ip.program[0]


def solve_part_b(part_b_input):

    for noun in range(100):
        for verb in range(100):
            # Structure input
            ip_input = part_b_input.split(',')
            ip_input[1] = noun
            ip_input[2] = verb

            ip = IntcodeProgram(ip_input)
            ip.run()

            if ip.program[0] == 19690720:
                return 100 * noun + verb


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2019, 2)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a, 'solve_func': solve_part_a,
                      'answer': pzl.answer_a if pzl.answered_a else None},
                'B': {'solved': pzl.answered_b, 'solve_func': solve_part_b,
                      'answer': pzl.answer_b if pzl.answered_b else None}}

    # Test inputs
    test_data = '1,0,0,0,99'

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
