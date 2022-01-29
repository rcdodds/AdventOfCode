# Libraries
from aocd.models import Puzzle
from aocd import submit
import logging

logging.basicConfig(level=logging.WARNING)

direction_vectors = {
    'U': (1, 0),
    'R': (0, 1),
    'D': (-1, 0),
    'L': (0, -1)
}


class ClosestIntersectionWire:
    def __init__(self, directions):
        self.coordinates = set()
        self.current = (0, 0)
        for d in directions:
            self.add_to_coordinates(d[0], int(d[1:]))

    def add_to_coordinates(self, letter, steps):
        vector = direction_vectors[letter]
        for _ in range(steps):
            self.current = (self.current[0] + vector[0], self.current[1] + vector[1])
            self.coordinates.add(self.current)


class EarliestIntersectionWire:
    def __init__(self, directions):
        self.coordinates = dict()
        self.current = (0, 0)
        self.total_steps = 0
        for d in directions:
            self.add_to_coordinates(d[0], int(d[1:]))

    def add_to_coordinates(self, letter, steps):
        vector = direction_vectors[letter]
        for _ in range(steps):
            self.current = (self.current[0] + vector[0], self.current[1] + vector[1])
            self.total_steps += 1
            if self.current not in self.coordinates.keys():
                self.coordinates[self.current] = self.total_steps


def solve_part_a(part_a_input):
    wire1, wire2 = (ClosestIntersectionWire(inputs.split(',')) for inputs in part_a_input.split('\n'))

    return min(map(sum, wire1.coordinates.intersection(wire2.coordinates)))


def solve_part_b(part_b_input):
    wire1, wire2 = (EarliestIntersectionWire(inputs.split(',')) for inputs in part_b_input.split('\n'))

    return min(map(lambda key: wire1.coordinates[key] + wire2.coordinates[key],
                   set(wire1.coordinates.keys()).intersection(set(wire2.coordinates.keys()))))


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2019, 3)
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
