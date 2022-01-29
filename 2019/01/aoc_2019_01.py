# Libraries
from aocd.models import Puzzle
from aocd import submit
import logging

logging.basicConfig(level=logging.WARNING)


def solve_part_a(part_a_input):
    return sum(map(lambda x: int(x) // 3 - 2, part_a_input.split('\n')))


def solve_part_b(part_b_input):
    total_fuel = 0
    to_be_considered = list(map(int, part_b_input.split('\n')))
    while to_be_considered:
        considering = to_be_considered.pop(0)
        fuel_needed = considering // 3 - 2
        if fuel_needed > 0:
            total_fuel += fuel_needed
            to_be_considered.append(fuel_needed)
    return total_fuel


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2019, 1)
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
