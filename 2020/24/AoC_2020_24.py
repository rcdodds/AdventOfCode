# Libraries
from aocd.models import Puzzle
from aocd import submit

neighbors = {'e': (0, 2), 'se': (1, 1), 'sw': (1, -1), 'w': (0, -2), 'nw': (-1, -1), 'ne': (-1, 1)}


def follow_instruction(instruction_str):
    global neighbors
    letter_list, row, col, next_instruction = list(instruction_str), 0, 0, ''

    while len(letter_list):
        next_instruction = next_instruction + letter_list.pop(0)
        if next_instruction in neighbors.keys():
            row += neighbors[next_instruction][0]
            col += neighbors[next_instruction][1]
            next_instruction = ''

    return row, col


def solve_part_a(part_a_input):
    flipped_tiles = tuple(follow_instruction(row) for row in part_a_input.split('\n'))
    return sum([int(flipped_tiles.count(tile) % 2 == 1) for tile in set(flipped_tiles)])


def solve_part_b(part_b_input):
    instructions = tuple(follow_instruction(row) for row in part_b_input.split('\n'))
    black_tiles = {t for t in instructions if instructions.count(t) % 2 == 1}

    for day in range(100):
        new_black, new_white = set(), set()
        rows, cols = tuple(tile[0] for tile in black_tiles), tuple(tile[1] for tile in black_tiles)
        for row in range(min(rows) - 1, max(rows) + 2):
            for col in range(min(cols) - 1, max(cols) + 2):
                neighbor_count = len(black_tiles.intersection({(row + n[0], col + n[1]) for n in neighbors.values()}))

                if (row + col) % 2 == 0:
                    if (row, col) in black_tiles and (neighbor_count == 0 or neighbor_count > 2):
                        new_white.add((row, col))
                    elif (row, col) not in black_tiles and neighbor_count == 2:
                        new_black.add((row, col))

        black_tiles = black_tiles.union(new_black)
        black_tiles = black_tiles.difference(new_white)

    return len(black_tiles)


if __name__ == '__main__':
    # Puzzle info
    test, solve, backtest = (False, True, False)
    (year, day) = (2020, 24)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a,
                      'answer': pzl.answer_a if pzl.answered_a else None,
                      'solve_func': solve_part_a},
                'B': {'solved': pzl.answered_b,
                      'answer': pzl.answer_b if pzl.answered_b else None,
                      'solve_func': solve_part_b}}

    # Test inputs
    # test_data = 'esew\nnwwswee'
    test_data = 'sesenwnenenewseeswwswswwnenewsewsw\nneeenesenwnwwswnenewnwwsewnenwseswesw\nseswneswswsenwwnwse\nnwnwneseeswswnenewneswwnewseswneseene\nswweswneswnenwsewnwneneseenw\neesenwseswswnenwswnwnwsewwnwsene\nsewnenenenesenwsewnenwwwse\nwenwwweseeeweswwwnwwe\nwsweesenenewnwwnwsenewsenwwsesesenwne\nneeswseenwwswnwswswnw\nnenwswwsewswnenenewsenwsenwnesesenew\nenewnwewneswsewnwswenweswnenwsenwsw\nsweneswneswneneenwnewenewwneswswnese\nswwesenesewenwneswnwwneseswwne\nenesenwswwswneneswsenwnewswseenwsese\nwnwnesenesenenwwnenwsewesewsesesew\nnenewswnwewswnenesenwnesewesw\neneswnwswnwsenenwnwnwwseeswneewsenese\nneswnwewnwnwseenwseesewsenwsweewe\nwseweeenwnesenwwwswnew'

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
