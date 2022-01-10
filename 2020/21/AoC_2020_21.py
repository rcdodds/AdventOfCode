# Libraries
from aocd.models import Puzzle
from aocd import submit
import re


def solve_puzzle(pzl_input, pzl_part):
    all_foreign = []
    option_dict = {}
    for row in pzl_input.split('\n'):
        foreign = re.findall(r'[a-z]+', row.split('(contains')[0])
        all_foreign.extend(foreign)
        known = re.findall(r'[a-z]+', row.split('(contains')[1])

        for known_allergen in known:
            if known_allergen not in option_dict.keys():
                option_dict[known_allergen] = set(foreign)
            else:
                option_dict[known_allergen] = option_dict[known_allergen].intersection(set(foreign))

    while max(map(len, option_dict.values())) > 1:
        for guessed in [g[1].copy().pop() for g in option_dict.items() if len(g[1]) == 1]:
            for unknown in option_dict.keys():
                if guessed in option_dict[unknown] and len(option_dict[unknown]) > 1:
                    option_dict[unknown].remove(guessed)

    for i in option_dict.keys():
        option_dict[i] = option_dict[i].pop()

    if pzl_part == 'A':
        return sum([f not in option_dict.values() for f in all_foreign])
    else:
        return ','.join([option_dict[allergen] for allergen in sorted(option_dict)])


if __name__ == '__main__':
    # Puzzle info
    test, solve, backtest = (False, True, False)
    (year, day) = (2020, 21)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a,
                      'answer': pzl.answer_a if pzl.answered_a else None,
                      'solve_func': solve_puzzle},
                'B': {'solved': pzl.answered_b,
                      'answer': pzl.answer_b if pzl.answered_b else None,
                      'solve_func': solve_puzzle}}

    # Test inputs
    test_data = 'mxmxvkd kfcds sqjhc nhms (contains dairy, fish)\n' \
                'trh fvjkl sbzzf mxmxvkd (contains dairy)\n' \
                'sqjhc fvjkl (contains soy)\n' \
                'sqjhc mxmxvkd sbzzf (contains fish) '

    # Consider both puzzles
    for part in pzl_dict.keys():
        if pzl_dict[part]['solved'] and not backtest:
            print(f'Year {year} Day {day} Part {part} already solved with answer = {pzl_dict[part]["answer"]}')
        else:
            # Attempt solution
            pzl_dict[part]['answer'] = pzl_dict[part]['solve_func'](pzl.input_data if not test else test_data, part)
            print(f'Year {year} Day {day} Part {part} answer = {pzl_dict[part]["answer"]}')

            # Submit if ready
            if solve and pzl_dict[part]['answer']:
                submit(pzl_dict[part]['answer'], part=part, year=year, day=day)
