# Libraries
from aocd.models import Puzzle
from aocd import submit


def solve_puzzle_part_dict(cup_str, prt):
    # Create dictionary of {cup: next_cup} pairs
    cup_list = list(map(int, cup_str))
    if prt == 'B':
        cup_list.extend(list(x for x in range(max(map(int, cup_str)) + 1, 1000001)))
    cup_map = dict(zip(cup_list, cup_list[1:] + cup_list[:1]))

    # Initialize
    start_cup = cup_list[0]

    max_r = 10000000 if prt == 'B' else 100
    for r in range(max_r):
        # Pick up next 3 cups
        pick_up = [cup_map[start_cup]]
        for _ in range(2):
            pick_up.append(cup_map[pick_up[-1]])

        # Find destination cup
        destination_cup = start_cup - 1 if start_cup > 1 else max(cup_list)
        while destination_cup in pick_up:
            destination_cup = destination_cup - 1 if destination_cup > 1 else max(cup_list)

        # Change mappings - e.g. (start) [pick_up] {destination} == (3) [8 9 1] {2} 5 >>> 3 2 8 9 1 5
        cup_map[start_cup] = cup_map[pick_up[-1]]           # Start cup now maps to the cup after the picked up cups
        cup_map[pick_up[-1]] = cup_map[destination_cup]     # Last picked up cup maps to cup after destination cup
        cup_map[destination_cup] = pick_up[0]               # Destination cup now maps to first picked up cup

        # Move to next start cup
        start_cup = cup_map[start_cup]

    if prt == 'B':
        return cup_map[1] * cup_map[cup_map[1]]
    else:
        result_list, next_num = [], cup_map[1]
        while next_num != 1:
            result_list.append(str(next_num))
            next_num = cup_map[next_num]
        return ''.join(result_list)


if __name__ == '__main__':
    # Puzzle info
    test, solve, backtest = (False, True, False)
    (year, day) = (2020, 23)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a,
                      'answer': pzl.answer_a if pzl.answered_a else None,
                      'solve_func': solve_puzzle_part_dict},
                'B': {'solved': pzl.answered_b,
                      'answer': pzl.answer_b if pzl.answered_b else None,
                      'solve_func': solve_puzzle_part_dict}}

    # Test inputs
    test_data = '389125467'

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
