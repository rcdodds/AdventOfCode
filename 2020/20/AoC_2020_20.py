# Libraries
from aocd.models import Puzzle
from aocd import submit
import numpy as np

offsets = {'up': (-1, 0), 'right': (0, 1), 'down': (1, 0), 'left': (0, -1)}


class Tile:
    def __init__(self, number, grid):
        self.number = number
        if isinstance(grid, list):
            self.grid = np.array([[cell == '#' for cell in tile_row] for tile_row in grid], dtype=np.int8)
        else:
            self.grid = grid

    def __repr__(self):
        return f'Tile #{self.number}'

    def turn(self):
        self.grid = np.rot90(self.grid, k=1, axes=(1, 0))

    def flip(self):
        self.grid = np.flip(self.grid, axis=1)

    def all_orientations(self):
        for _ in range(2):
            for _ in range(4):
                self.turn()
                yield
            self.flip()

    def match(self, **neighbors):
        for neighbor in neighbors.items():
            assert isinstance(neighbor[1], Tile)
            if neighbor[0] == 'up':
                if np.array_equal(self.grid[0], neighbor[1].grid[-1]):
                    break
                else:
                    return False
            elif neighbor[0] == 'right':
                if np.array_equal(self.grid[:, -1], neighbor[1].grid[:, 0]):
                    break
                else:
                    return False
            elif neighbor[0] == 'down':
                if np.array_equal(self.grid[-1], neighbor[1].grid[0]):
                    break
                else:
                    return False
            elif neighbor[0] == 'left':
                if np.array_equal(self.grid[:, 0], neighbor[1].grid[:, -1]):
                    break
                else:
                    return False
        return True

    def remove_border(self):
        self.grid = self.grid[1:-1, 1:-1]


def match_tiles(input_str):
    global offsets
    free_tiles = {Tile(int(tile_input.split(':')[0].split(' ')[1]), tile_input.split(':\n')[1].split('\n'))
                  for tile_input in input_str.split('\n\n')}
    tile_dict = {(0, 0): free_tiles.pop()}      # Fix the first tile at (0, 0)

    while free_tiles:
        evaluate_tile = free_tiles.pop()
        open_spots = {(fixed[0] + o[0], fixed[1] + o[1])
                      for fixed in tile_dict.keys() for o in offsets.values()}.difference(set(tile_dict.keys()))

        # Evaluate the chosen tile in any orientation for all open spots
        spot_found = False
        for _ in evaluate_tile.all_orientations():
            for spot in open_spots:
                neighbor_dict = {o[0]: tile_dict.get((spot[0] + o[1][0], spot[1] + o[1][1]))
                                 for o in offsets.items() if tile_dict.get((spot[0] + o[1][0], spot[1] + o[1][1]))}
                if evaluate_tile.match(**neighbor_dict):
                    spot_found = True
                    tile_dict[spot] = evaluate_tile
                    break
            if spot_found:
                break

        if not spot_found:
            free_tiles.add(evaluate_tile)

    return tile_dict


def merge_tiles(tile_dictionary):
    rows = {coordinate[0] for coordinate in tile_dictionary.keys()}
    cols = {coordinate[1] for coordinate in tile_dictionary.keys()}

    row_arrays = []
    for row in range(min(rows), max(rows) + 1, 1):
        for col in range(min(cols), max(cols) + 1, 1):
            tile_dictionary[(row, col)].remove_border()
            if col == min(cols):
                row_array = tile_dictionary[(row, col)].grid
            else:
                row_array = np.concatenate((row_array, tile_dictionary[(row, col)].grid), axis=1)

                if col == max(cols):
                    row_arrays.append(row_array)
    return Tile('ALL', np.concatenate(row_arrays, axis=0))


def solve_part_a(part_a_input):
    tile_dict = match_tiles(part_a_input)

    # Find corners
    rows = {coordinate[0] for coordinate in tile_dict.keys()}
    cols = {coordinate[1] for coordinate in tile_dict.keys()}
    corner_tiles = [tile_dict[(min(rows), min(cols))].number, tile_dict[(min(rows), max(cols))].number,
                    tile_dict[(max(rows), min(cols))].number, tile_dict[(max(rows), max(cols))].number]
    return np.product(corner_tiles, dtype=np.int64)


def solve_part_b(part_b_input):
    image_dict = match_tiles(part_b_input)
    full_image = merge_tiles(image_dict)

    search_str = '                  # \n#    ##    ##    ###\n #  #  #  #  #  #   '
    search = np.array([[c == '#' for c in r] for r in search_str.split('\n')], dtype=np.int8)

    orientation = full_image.all_orientations()
    search_matches = 0
    while not search_matches:
        for xy, cell in np.ndenumerate(full_image.grid):
            # Need to be able to extract the full image
            if xy[0]+search.shape[0] < full_image.grid.shape[0] and xy[1]+search.shape[1] < full_image.grid.shape[1]:
                check_array = full_image.grid[xy[0]:xy[0]+search.shape[0], xy[1]:xy[1]+search.shape[1]]

                if np.all(check_array[np.nonzero(search)]):
                    search_matches += 1
        next(orientation)

    return np.count_nonzero(full_image.grid) - search_matches * np.count_nonzero(search)


if __name__ == '__main__':
    # Puzzle info
    test, solve, backtest = (False, True, False)
    (year, day) = (2020, 20)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a,
                      'answer': pzl.answer_a if pzl.answered_a else None,
                      'solve_func': solve_part_a},
                'B': {'solved': pzl.answered_b,
                      'answer': pzl.answer_b if pzl.answered_b else None,
                      'solve_func': solve_part_b}}

    # Test inputs
    test_data = 'Tile 2311:\n..##.#..#.\n##..#.....\n#...##..#.\n####.#...#\n##.##.###.\n##...#.###\n.#.#.#..##\n' \
                '..#....#..\n###...#.#.\n..###..###\n\nTile ' \
                '1951:\n#.##...##.\n#.####...#\n.....#..##\n#...######\n.##.#....#\n.###.#####\n###.##.##.\n' \
                '.###....#.\n..#.#..#.#\n#...##.#..\n\nTile ' \
                '1171:\n####...##.\n#..##.#..#\n##.#..#.#.\n.###.####.\n..###.####\n.##....##.\n.#...####.\n' \
                '#.##.####.\n####..#...\n.....##...\n\nTile ' \
                '1427:\n###.##.#..\n.#..#.##..\n.#.##.#..#\n#.#.#.##.#\n....#...##\n...##..##.\n...#.#####\n' \
                '.#.####.#.\n..#..###.#\n..##.#..#.\n\nTile ' \
                '1489:\n##.#.#....\n..##...#..\n.##..##...\n..#...#...\n#####...#.\n#..#.#.#.#\n...#.#.#..\n' \
                '##.#...##.\n..##.##.##\n###.##.#..\n\nTile ' \
                '2473:\n#....####.\n#..#.##...\n#.##..#...\n######.#.#\n.#...#.#.#\n.#########\n.###.#..#.\n' \
                '########.#\n##...##.#.\n..###.#.#.\n\nTile ' \
                '2971:\n..#.#....#\n#...###...\n#.#.###...\n##.##..#..\n.#####..##\n.#..####.#\n#..#.#..#.\n' \
                '..####.###\n..#.#.###.\n...#.#.#.#\n\nTile ' \
                '2729:\n...#.#.#.#\n####.#....\n..#.#.....\n....#..#.#\n.##..##.#.\n.#.####...\n####.#.#..\n' \
                '##.####...\n##..#.##..\n#.##...##.\n\nTile ' \
                '3079:\n#.#.#####.\n.#..######\n..#.......\n######....\n####.#..#.\n.#...#.##.\n#.#####.##\n' \
                '..#.###...\n..#.......\n..#.###...'

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
