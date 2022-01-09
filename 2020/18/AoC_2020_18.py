# Libraries
from aocd.models import Puzzle
from aocd import submit
import math


def evaluate_line(line, method):
    # Initialize
    result, operator, pos = (0, '+', 0)
    all_results, restart = [], False    # Only used when method != 'left_to_right'

    while pos <= len(line) - 1:
        if line[pos] in ['+', '*']:
            operator = line[pos]
            pos += 1
        else:
            # Evaluate the line inside the outermost, matching pair of parentheses
            if line[pos] == '(':
                # Find the matching end parentheses
                offset, close_paren_to_find = 0, 1
                while close_paren_to_find:
                    offset += 1
                    if line[pos+offset] == '(':
                        close_paren_to_find += 1
                    elif line[pos+offset] == ')':
                        close_paren_to_find -= 1
                next_num = evaluate_line(line[pos + 1:pos + offset], method)
                pos += offset + 1
            # Number found - increase result
            elif line[pos].isnumeric():
                next_num = int(line[pos])
                pos += 1

            # Perform operation
            if operator == '+':
                result += next_num
            elif operator == '*':
                if method == 'left_to_right':
                    result *= next_num
                else:
                    all_results.append(result)
                    result = next_num

    if method == 'left_to_right':
        return result
    else:
        return math.prod(all_results) * result


def solve_part_a(part_a_input):
    return sum([evaluate_line(list(row.replace(' ', '')), 'left_to_right') for row in part_a_input.split('\n')])


def solve_part_b(part_b_input):
    return sum([evaluate_line(list(row.replace(' ', '')), 'add_first') for row in part_b_input.split('\n')])


if __name__ == '__main__':
    # Puzzle info
    test, solve, backtest = (False, True, False)
    (year, day) = (2020, 18)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a,
                      'answer': pzl.answer_a if pzl.answered_a else None,
                      'solve_func': solve_part_a},
                'B': {'solved': pzl.answered_b,
                      'answer': pzl.answer_b if pzl.answered_b else None,
                      'solve_func': solve_part_b}}

    # Test inputs
    test_data = '1 + 2 * 3 + 4 * 5 + 6\n' \
                '1 + (2 * 3) + (4 * (5 + 6))\n' \
                '2 * 3 + (4 * 5)\n' \
                '5 + (8 * 3 + 9 + 3 * 4 * 3)\n' \
                '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))\n' \
                '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'

    # Consider both puzzles
    for part in pzl_dict.keys():
        if pzl_dict[part]['solved'] and not backtest:
            print(f'Year {year} Day {day} Part {part} already solved with answer = {pzl_dict[part]["answer"]}')
        else:
            # Attempt solution
            pzl_dict[part]['answer'] = pzl_dict[part]['solve_func'](pzl.input_data if not test else test_data)
            print(f'Year {year} Day {day} Part {part} answer = {pzl_dict[part]["answer"]}')

            # Submit if ready
            if solve and pzl_dict[part]['answer']:
                submit(pzl_dict[part]['answer'], part=part, year=year, day=day)
