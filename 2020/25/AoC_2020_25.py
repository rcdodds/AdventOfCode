# Libraries
from aocd.models import Puzzle
from aocd import submit


def find_loop_size(p_keys):
    loop_size, result = 0, 1
    while result not in p_keys:
        loop_size += 1
        result = (result * 7) % 20201227
    return loop_size, result


def solve_part_a(public_keys):
    loop_size, cracked_key = find_loop_size(public_keys)
    remaining_key = public_keys[1] if cracked_key == public_keys[0] else public_keys[0]
    encryption_key = pow(remaining_key, loop_size, 20201227)
    return encryption_key


if __name__ == '__main__':
    # Puzzle info
    test, solve, backtest = (False, True, False)
    (year, day) = (2020, 25)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a,
                      'answer': pzl.answer_a if pzl.answered_a else None,
                      'solve_func': solve_part_a}}

    # Test inputs
    test_data = '5764801\n17807724'

    # Consider both puzzles
    for part in pzl_dict.keys():
        if pzl_dict[part]['solved'] and not backtest:
            print(f'Year {year} Day {day} Part {part} already solved with answer = {pzl_dict[part]["answer"]}')
        else:
            # Attempt solution
            keys = tuple(map(int, pzl.input_data.split('\n') if not test else test_data.split('\n')))
            pzl_dict[part]['answer'] = pzl_dict[part]['solve_func'](keys)
            print(f'Year {year} Day {day} Part {part} answer = {pzl_dict[part]["answer"]}')

            # Submit if ready
            if solve and pzl_dict[part]['answer']:
                submit(pzl_dict[part]['answer'], part=part, year=year, day=day)
