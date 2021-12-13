# Libraries
import networkx as nx
from aocd.models import Puzzle
from aocd import submit
from aoc_util import DFS


class CaveSystem:
    def __init__(self, path_list):
        # Split input into graph data
        nodes = set()
        edges = []
        for row in path_list:
            pieces = row.split('-')
            nodes.update(pieces)
            edges.append(tuple(pieces))

        # Construct graph
        self.CaveGraph = nx.Graph()
        self.CaveGraph.add_nodes_from(nodes)
        self.CaveGraph.add_edges_from(edges)

        # Initialize path property
        self.path_count = 0


def solve_puzzle(pzl_data, letter):
    cave = CaveSystem(pzl_data)

    if letter == 'A':
        return DFS.find_all_paths(cave.CaveGraph, source='start', target='end',
                                  history=['start'], visit_small_caves_once=True)

    elif letter == 'B':
        return DFS.find_all_paths(cave.CaveGraph, source='start', target='end',
                                  history=['start'], visit_small_caves_once=False)


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 12)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    puzzle_data = puzzle.input_data.split('\n')
    # puzzle_data = 'start-A\nstart-b\nA-c\nA-b\nb-d\nA-end\nb-end'.split('\n')
    # puzzle_data = 'dc-end\nHN-start\nstart-kj\ndc-start\ndc-HN\nLN-dc\nHN-end\nkj-sa\nkj-HN\nkj-dc'.split('\n')

    # Consider both puzzles
    for part in ['A', 'B']:
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(puzzle_data, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
