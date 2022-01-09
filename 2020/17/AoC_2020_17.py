# Libraries
from aocd.models import Puzzle
from aocd import submit
from aoc_util import GrowingArray as ga


def grow_grid(part_a_input, dim):
    cubes = ga.GrowingArray(row_strs=part_a_input.split('\n'), on_char='#', dimensions=dim)
    for _ in range(6):
        cubes.grow(activate_counts=[3], remain_active_counts=[2, 3])
    return cubes.count_on()


if __name__ == '__main__':
    # Puzzle info
    testing, ready_to_solve, backtesting = (False, True, True)
    (year, day) = (2020, 17)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a,
                      'answer': pzl.answer_a if pzl.answered_a else None,
                      'dim': 3},
                'B': {'solved': pzl.answered_b,
                      'answer': pzl.answer_b if pzl.answered_b else None,
                      'dim': 4}}

    # Test inputs
    test_data = '.#.\n..#\n###'

    # Consider both puzzles
    for part in pzl_dict.keys():
        if pzl_dict[part]['solved'] and not backtesting:
            print(f'Year {year} Day {day} Part {part} already solved with answer = {pzl_dict[part]["answer"]}')
        else:
            # Attempt solution
            pzl_dict[part]['answer'] = grow_grid(pzl.input_data if not testing else test_data, pzl_dict[part]['dim'])
            print(f'Year {year} Day {day} Part {part} answer = {pzl_dict[part]["answer"]}')

            # Submit if ready
            if ready_to_solve and pzl_dict[part]['answer']:
                submit(pzl_dict[part]['answer'], part=part, year=year, day=day)
