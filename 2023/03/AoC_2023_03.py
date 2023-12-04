# Libraries
from aocd.models import Puzzle
from aocd import submit
import logging
import re

logging.basicConfig(level=logging.WARNING)


def solve_part_a(part_a_input):
    score = 0
    rows = part_a_input.split('\n')
    for row_index, row_str in enumerate(rows):
        number_matches = re.finditer(r'\d+', row_str)
        for m in number_matches:
            symbol_matches = re.finditer(r'[^\d.]', "".join([r[max(0, m.span()[0] - 1):min(len(r), m.span()[1] + 1)]
                                                             for r in rows[max(0, row_index-1):
                                                                           min(len(rows), row_index+2)]]))
            if len([x for x in symbol_matches]) > 0:
                score += int(m.group())
    return score


def solve_part_b(part_b_input):
    score = 0
    rows = part_b_input.split('\n')
    part_num_dict = dict()
    for row_index, row_str in enumerate(rows):
        num_matches = re.finditer(r'\d+', row_str)
        # Loop through part numbers found
        for num_match in num_matches:
            # Check row above, same row, and row below
            for row_offset in range(3):
                eval_row_index = row_index + row_offset - 1
                # Only proceed with check if row index exists
                if 0 <= eval_row_index < len(rows):
                    star_matches = re.finditer(r'\*', rows[eval_row_index])
                    # Loop through stars found in 3 corresponding rows
                    for star_match in star_matches:
                        # Only proceed with logging if star is adjacent to part number
                        if num_match.start() - 1 <= star_match.start() <= num_match.end():
                            part_num = int(num_match.group())
                            star_index = eval_row_index * len(row_str) + star_match.start() + 1
                            # Check if part num already has running list of stars in dictionary
                            if part_num in part_num_dict.keys() and part_num_dict[part_num] is not None:
                                part_num_dict[part_num].append(star_index)
                            else:
                                part_num_dict[part_num] = [star_index]

    # Determine which stars have 2 part numbers bordering
    all_stars = [y for x in part_num_dict.values() for y in x if x is not None and y is not None]
    for star in set(all_stars):
        part_numbers = []
        for pn in part_num_dict.keys():
            if part_num_dict[pn] is not None and star in part_num_dict[pn]:
                part_numbers.append(pn)

        # Score star if suitable
        if len(part_numbers) == 2:
            score += part_numbers[0] * part_numbers[1]

    return score


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2023, 3)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a, 'solve_func': solve_part_a,
                      'answer': pzl.answer_a if pzl.answered_a else None},
                'B': {'solved': pzl.answered_b, 'solve_func': solve_part_b,
                      'answer': pzl.answer_b if pzl.answered_b else None}}

    # Test inputs
    test_data = '467..114..\n...*......\n..35..633.\n......#...\n617*......\n.....+.58.\n..592.....\n......755.\n...$.*....\n.664.598..'

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
