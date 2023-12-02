# Libraries
from aocd.models import Puzzle
from aocd import submit
import logging
import re

logging.basicConfig(level=logging.WARNING)


def solve_part_a(part_a_input):
    impossible_game_sum = 0
    for row in part_a_input.split('\n'):
        groups = re.findall(r'(1[5-9] (green|blue|red))|(14 (red|green))|(13 red)|([2-9]\d)|(\d{3,})', row.split(':')[-1])
        impossibilities = [match for matches in list(filter(lambda x: x is not None, groups))
                           for match in matches if match != '']
        if len(impossibilities) == 0:
            impossible_game_sum += int(re.findall(r'\s(\d*):', row)[0])
        print(int(re.findall(r'\s(\d*):', row)[0]), " >> Possible:", str(len(impossibilities) == 0), " >> ", impossibilities)
    return impossible_game_sum


def solve_part_b(part_b_input):
    impossible_game_sum = 0
    for row in part_b_input.split('\n'):
        product = 1
        for color in ['red', 'green', 'blue']:
            print([int(x) for x in re.findall(r'(\d*) ' + color, row)])
            product *= max([int(x) for x in re.findall(r'(\d*) ' + color, row)])
        impossible_game_sum += product
    return impossible_game_sum


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2023, 2)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a, 'solve_func': solve_part_a,
                      'answer': pzl.answer_a if pzl.answered_a else None},
                'B': {'solved': pzl.answered_b, 'solve_func': solve_part_b,
                      'answer': pzl.answer_b if pzl.answered_b else None}}

    # Test inputs
    test_data = 'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\nGame 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\nGame 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\nGame 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\nGame 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'

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
