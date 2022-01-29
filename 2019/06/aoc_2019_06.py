# Libraries
import logging
import networkx as nx
from aocd.models import Puzzle
from aocd import submit

logging.basicConfig(level=logging.WARNING)


def solve_part_a(part_a_input):
    orbit_graph = nx.DiGraph()
    orbit_graph.add_edges_from([(r.split(')')[1], r.split(')')[0]) for r in part_a_input.split('\n')])
    total_orbits = 0
    for planet in orbit_graph:
        current = planet
        while current != 'COM':
            current = list(orbit_graph.successors(current))[0]
            total_orbits += 1
    return total_orbits


def solve_part_b(part_b_input):
    orbit_graph = nx.Graph()
    orbit_graph.add_edges_from([(r.split(')')[1], r.split(')')[0]) for r in part_b_input.split('\n')])
    reachable = nx.shortest_path(orbit_graph, 'YOU', 'SAN')
    return len(reachable) - 3


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2019, 6)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a, 'solve_func': solve_part_a,
                      'answer': pzl.answer_a if pzl.answered_a else None},
                'B': {'solved': pzl.answered_b, 'solve_func': solve_part_b,
                      'answer': pzl.answer_b if pzl.answered_b else None}}

    # Test inputs
    test_data = 'COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L'
    test_data = 'COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN'

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
