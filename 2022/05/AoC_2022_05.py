# Libraries
from aocd.models import Puzzle
from aocd import submit
import logging

logging.basicConfig(level=logging.WARNING)

START_STACKS = [
    ['G', 'D', 'V', 'Z', 'J', 'S', 'B'],
    ['Z', 'S', 'M', 'G', 'V', 'P'],
    ['C', 'L', 'B', 'S', 'W', 'T', 'Q', 'F'],
    ['H', 'J', 'G', 'W', 'M', 'R', 'V', 'Q'],
    ['C', 'L', 'S', 'N', 'F', 'M', 'D'],
    ['R', 'G', 'C', 'D'],
    ['H', 'G', 'T', 'R', 'J', 'D', 'S', 'Q'],
    ['P', 'F', 'V'],
    ['D', 'R', 'S', 'T', 'J']
]


def solve_part_a(part_a_input):
    stacks = START_STACKS
    for instruction in part_a_input.split('\n'):
        if instruction[:4] == 'move':
            instruction_componentes = instruction.split(' ')
            for count in range(int(instruction_componentes[1])):
                x = stacks[int(instruction_componentes[3]) - 1].pop()
                stacks[int(instruction_componentes[5]) - 1].append(x)
    return ''.join([stack[-1] for stack in stacks])


def solve_part_b(part_b_input):
    stacks = START_STACKS
    for instruction in part_b_input.split('\n'):
        if instruction[:4] == 'move':
            instruction_componentes = instruction.split(' ')
            stacks[int(instruction_componentes[5]) - 1].extend(
                stacks[int(instruction_componentes[3]) - 1][-1 * int(instruction_componentes[1]):]
            )
            for count in range(int(instruction_componentes[1])):
                x = stacks[int(instruction_componentes[3]) - 1].pop()
    return ''.join([stack[-1] for stack in stacks])


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, False)
    (year, day) = (2022, 5)
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
