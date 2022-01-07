# Libraries
from aocd.models import Puzzle
from aocd import submit
import numpy as np
from collections import defaultdict
import itertools


class Scanner:
    def __init__(self, number, beacons):
        self.number = number
        self.position = None
        self.beacons = np.array(beacons, dtype=int)
        self.vectors = None
        self.calculate_distance_vectors()

    def __repr__(self):
        return f'Scanner #{str(self.number).zfill(3)}\n{self.beacons}'

    def calculate_distance_vectors(self):
        """
        Vectors from each beacon to every other beacon. Used for comparing scanners.
        """
        vectors = defaultdict(set)
        for start_pt, end_pt in itertools.combinations((tuple(bcn) for bcn in self.beacons), 2):
            vectors[start_pt].add((end_pt[0] - start_pt[0], end_pt[1] - start_pt[1], end_pt[2] - start_pt[2]))
            vectors[end_pt].add((start_pt[0] - end_pt[0], start_pt[1] - end_pt[1], start_pt[2] - end_pt[2]))
        self.vectors = vectors

    def fix_position(self, position):
        """
        Fix the scanner at a particular coordinate
        """
        self.position = position                        # Fix the scanner's position in 3D space
        for i in range(3):
            self.beacons[:, i] += self.position[i]      # Move beacons from relative positions to absolute positions
        self.calculate_distance_vectors()               # Reset distance vectors

    def turn(self):
        """
        Rotate the beacons 90-degrees in the clockwise direction about the x-axis
        i.e. Leave the cube flat on the table but turn it clockwise 90-degrees
        e.g. (1, 2, 3) >> (1, 3, -2)
        """
        turned = np.zeros_like(self.beacons, dtype=int)
        turned[:, 0] = self.beacons[:, 0]   # +X remains the same
        turned[:, 1] = self.beacons[:, 2]   # +Z becomes the new +Y
        turned[:, 2] = -self.beacons[:, 1]  # -Y becomes the new +Z
        self.beacons = turned
        self.calculate_distance_vectors()   # Reset distance vectors

    def roll(self):
        """
        Rotate the beacons 90-degrees in the clockwise direction about the z-axis
        i.e. Roll the cube away from you
        e.g. (1, 2, 3) >> (-2, 1, 3)
        """
        rolled = np.zeros_like(self.beacons, dtype=int)
        rolled[:, 0] = -self.beacons[:, 1]  # -Y becomes the new +X
        rolled[:, 1] = self.beacons[:, 0]   # +X becomes the new +Y
        rolled[:, 2] = self.beacons[:, 2]   # +Z remains the same
        self.beacons = rolled
        self.calculate_distance_vectors()   # Reset distance vectors

    def all_rotations(self):
        for _ in range(2):      # Start outer sequence with top side and then again with bottom side
            for _ in range(3):      # Start inner sequence with the 3 sides reachable from the starting side
                self.roll()             # Inner sequence step 1 = Roll
                yield

                for _ in range(3):
                    self.turn()         # Inner sequence step 2-4 = Turn, Turn, Turn
                    yield

            # Flip from top side to bottom side
            self.roll()
            self.turn()
            self.roll()

    def overlap(self, other_scanners):
        for other_scanner in other_scanners:        # Compare this scanner to all previously matched scanners
            for this_distances in self.vectors.items():   # Compare a single point from this scanner...
                for other_distances in other_scanner.vectors.items():     # To all points from the other scanner...
                    common_distance_vectors = this_distances[1].intersection(other_distances[1])
                    if len(common_distance_vectors) >= 11:  # Sharing 11 vectors = 12 common beacons = overlap
                        print(f'Scanner {self.number} has been matched with scanner {other_scanner.number}')
                        self.fix_position((other_distances[0][0] - this_distances[0][0],
                                           other_distances[0][1] - this_distances[0][1],
                                           other_distances[0][2] - this_distances[0][2]))
                        return True
        return False


def match_scanners(scanner_inputs):
    # Instantiate all scanner objects
    unmatched_scanners = [Scanner(i, beacon_list) for i, beacon_list in enumerate(scanner_inputs)]
    matched_scanners = []

    # Define the first scanner to be at the origin
    scanner = unmatched_scanners.pop(0)
    scanner.fix_position(np.zeros((3,), dtype=int))
    matched_scanners.append(scanner)

    while unmatched_scanners:
        scanner = unmatched_scanners.pop(0)     # Get the next unmatched scanner to be considered
        assert isinstance(scanner, Scanner)     # Confirm we're dealing with a scanner object
        orientation = scanner.all_rotations()   # Generator object of all 24 possible orientations
        matched = False                         # Assume match will not be found

        while not matched:
            # Only continue if there's another orientation to check
            try:
                next(orientation)
            except StopIteration:
                break

            # Check if this orientation has 12 beacons in common with previously matched scanners
            matched = scanner.overlap(matched_scanners)

        # Log the match for comparing future scanners
        if matched:
            matched_scanners.append(scanner)
        else:
            # Match has not been found. Scanner must be considered again later.
            unmatched_scanners.append(scanner)

    return matched_scanners


def unique_beacons(list_of_scanners):
    """
    Consolidate beacons from overlapping scanners into a unique set
    """
    return set(tuple(coord_array) for scanner in list_of_scanners for coord_array in scanner.beacons)


def manhattan_dist(p, q):
    """
    Calculate manhattan distance between two n-length tuples
    """
    assert len(p) == len(q)
    return sum([abs(p[i]-q[i]) for i in range(len(p))])


def max_manhattan_distance(scanner_objs):
    """
    Maximum Manhattan distance between two scanner objects evaluated pairwise
    """
    return max([manhattan_dist(pair[0].position, pair[1].position) for pair in itertools.combinations(scanner_objs, 2)])


if __name__ == '__main__':
    # Get & format puzzle data
    (year, day) = (2021, 19)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data

    scanners_list = []
    for scanner_str in puzzle_data.split('\n\n'):
        scanner_list = []
        for beacon_str in scanner_str.split('\n'):
            if 'scanner' not in beacon_str:
                scanner_list.append(list(map(int, beacon_str.split(','))))
        scanners_list.append(scanner_list)

    # Solve a part of the puzzle
    matched_scanner_objects = match_scanners(scanners_list)
    if not puzzle.answered_a:
        submit(len(unique_beacons(matched_scanner_objects)), part='A', year=year, day=day)
    elif not puzzle.answered_b:
        submit(max_manhattan_distance(matched_scanner_objects), part='B', year=year, day=day)
    else:
        print(f'Puzzle for year {year} // day {day} already solved!\n'
              f'Answer for part A = {puzzle.answer_a}\n'
              f'Answer for part B = {puzzle.answer_b}')
