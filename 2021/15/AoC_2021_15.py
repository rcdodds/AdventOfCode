# Libraries
import numpy as np
import networkx as nx
from aocd.models import Puzzle
from aocd import submit


class ChitonGraph:
    def __init__(self, input_str):
        # Basic information
        self.i = input_str.count('\n') + 1
        self.j = input_str.find('\n')
        self.source = 0
        self.target = (self.i * self.j) - 1
        self.risk_str = input_str.replace('\n', '')

        # Create unweighted graph with all nodes
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from([i for i in range(self.i * self.j)])

        # Add weighted edges
        for node_counter, risk_char in enumerate(self.risk_str):
            # This node can be reached from above (everything except top row)
            if node_counter >= self.j:
                self.graph.add_edge(node_counter - self.j, node_counter, weight=int(risk_char))
            # Node can be reached from below (everything except bottom row)
            if node_counter < ((self.i * self.j) - self.j):
                self.graph.add_edge(node_counter + self.j, node_counter, weight=int(risk_char))
            # Node can be reached from right (everything except left column)
            if node_counter % self.j:
                self.graph.add_edge(node_counter - 1, node_counter, weight=int(risk_char))
            # Node can be reached from left (everything except right column)
            if (node_counter + 1) % self.j:
                self.graph.add_edge(node_counter + 1, node_counter, weight=int(risk_char))

    def find_least_risky_path(self):
        safest_path_nodes = nx.shortest_path(self.graph, self.source, self.target, weight='weight')
        safest_path_risks = [int(self.risk_str[node]) for node in safest_path_nodes]
        total_risk = sum(safest_path_risks[1:])
        return safest_path_nodes, safest_path_risks, total_risk


def solve_puzzle(pzl_data_str, letter):

    if letter == 'A':
        cave_str = pzl_data_str
    elif letter == 'B':
        cave_str_list = []
        for j in range(5):
            for row in pzl_data_str.split('\n'):
                new_row_list = []
                for i in range(5):
                    for digit in row:
                        new_digit = int(digit) + i + j
                        if new_digit > 9:
                            new_digit = new_digit % 9
                        new_row_list.append(str(new_digit))
                cave_str_list.append(''.join(new_row_list))
        cave_str = '\n'.join(cave_str_list)

    # Create instance of graph class
    Graph = ChitonGraph(cave_str)
    # Return total risk of safest path
    nodes, risks, total = Graph.find_least_risky_path()
    return total


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 15)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle input
    puzzle_data = puzzle.input_data
    # puzzle_data = '1163751742\n1381373672\n2136511328\n3694931569\n7463417111\n1319128137\n1359912421\n3125421639\n1293138521\n2311944581'

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
