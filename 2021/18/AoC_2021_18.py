# Libraries
from anytree import Node, RenderTree, PreOrderIter
import math
from itertools import permutations
from aocd.models import Puzzle
from aocd import submit


class ActionComplete(Exception):
    pass


class SnailfishTree:
    def __init__(self, nested_list):
        self.root = Node(None)
        build_tree(nested_list, self.root)

    def add_tree(self, tree2):
        # Create new root node
        new_root = Node(None)

        # Assign both the current tree.png and the second tree.png as children of the new root node
        self.root.parent = new_root
        tree2.root.parent = new_root

        # Store the new root node as this tree.png's root
        self.root = new_root

    def reduce(self):
        while True:
            try:
                # Explode pairs at level 4 or deeper
                self.explode()
                # Split anything >= 10
                self.split()
                # If no actions were performed, this reduction is complete
                break

            # Action was performed - restart reductions
            except ActionComplete:
                continue

    def explode(self):
        # Initialize searching variables
        skip = False
        left_node = None
        to_add_right = None

        # Get list of nodes from tree.png iterator (need to check for reaching end of tree.png
        node_list = list(PreOrderIter(self.root))

        # Traverse tree.png from left to right
        for node in node_list:
            # Skip second node in pair to be exploded
            if skip:
                skip = False
                continue

            # Look for are any pairs at level 4 or below
            if to_add_right is None and node.depth > 4 and isinstance(node.name, int) and \
                    node.siblings and isinstance(node.siblings[0].name, int):
                # print(f'MUST EXPLODE - [{node.name}, {node.siblings[0].name}]')

                # Add left value of pair to the most recent regular number on the left (if one exists)
                if left_node is not None:
                    left_node.name = left_node.name + node.name

                # Store right value of pair which will be added to the next regular number found (if one exists)
                to_add_right = node.siblings[0].name

                # Remove exploded pair after setting parent to 0
                node.parent.name = 0
                node.siblings[0].parent = None
                node.parent = None

                # Set flag to ignore second node in this pair
                skip = True

            # Found a regular number
            elif isinstance(node.name, int):
                # Still searching for pair to explode - save this node as the current left node
                if to_add_right is None:
                    left_node = node
                # Pair has already been exploded
                else:
                    # Add the stored value to this node
                    node.name = node.name + to_add_right

                    # Explosion complete - start new search
                    raise ActionComplete

            # Pair has been exploded but end of iterator was reached without finding regular number to right
            elif to_add_right and node_list.index(node) == len(node_list):
                # Explosion complete - start new search
                raise ActionComplete

    def split(self):
        # Traverse tree.png from left to right
        for node in PreOrderIter(self.root):
            # Look for are any pairs at level 4 or below
            if isinstance(node.name, int) and node.name >= 10:
                # print(f'MUST SPLIT - {node.name} >> {[math.floor(node.name / 2), math.ceil(node.name / 2)]}')

                # Split node into floor / ceiling of division by two
                left_child = Node(math.floor(node.name / 2), parent=node)
                right_child = Node(math.ceil(node.name / 2), parent=node)

                # This node is now a parent node (no value)
                node.name = None

                # Raise an exception to indicate an action has been made
                raise ActionComplete


def find_magnitude(start_node):
    # Initialize
    magnitude = 0

    # If the node is an integer, return it
    if isinstance(start_node.name, int):
        magnitude += start_node.name
    # Otherwise, find magnitudes of child nodes
    else:
        magnitude += (3 * find_magnitude(start_node.children[0]))
        magnitude += (2 * find_magnitude(start_node.children[1]))

    return magnitude


def build_tree(tree_input, parent=None):
    # Loop through values in list
    for element in tree_input:
        # List? Add another internal node and recurse to next level
        if isinstance(element, list):
            node = Node(None, parent)
            build_tree(element, parent=node)

        # Integer? Add value, done this level
        else:
            node = Node(element, parent)


def solve_puzzle(pzl_data, letter):
    if letter == 'A':
        # Initialize
        main_tree = None

        # Loop through snailfish numbers
        for sf_num in pzl_data:
            # If this is the first number, initialize the main tree.png.
            if not main_tree:
                main_tree = SnailfishTree(sf_num)

            # Otherwise, add the new number to the main tree.png.
            else:
                # Add trees
                main_tree.add_tree(SnailfishTree(sf_num))

                # Reduce until stable
                main_tree.reduce()

        return find_magnitude(main_tree.root)

    elif letter == 'B':
        possible_magnitudes = []
        # Find all possibilities from the input
        for perm in permutations(pzl_data, 2):
            # Set up tree
            tree = SnailfishTree(perm[0])
            # Do addition
            tree.add_tree(SnailfishTree(perm[1]))
            # Reduce as much as necessary
            tree.reduce()
            # Find magnitude
            mag = find_magnitude(tree.root)
            # Store
            possible_magnitudes.append(mag)

        return max(possible_magnitudes)


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 18)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle tree_input
    puzzle_data = [
        [[2, [2, 3]], [[[0, 0], [2, 2]], [[3, 3], [3, 5]]]],
        [[[8, [8, 8]], 6], [9, 5]],
        [[[[5, 2], 3], [[5, 8], [1, 1]]], [[[4, 2], 3], [[1, 6], 4]]],
        [[[[6, 8], [0, 9]], 8], [[[9, 4], 6], [8, 6]]],
        [9, [[6, 7], 4]],
        [[1, [3, 6]], [5, [[7, 4], 6]]],
        [[[[4, 7], 6], [[8, 9], 5]], [[[6, 2], [2, 7]], [[9, 0], [7, 0]]]],
        [[[[7, 3], 4], [7, [7, 4]]], 1],
        [4, [6, 6]],
        [[3, [3, 2]], [[7, 1], [[6, 4], [6, 1]]]],
        [[[[8, 7], 4], 8], [[[8, 9], 5], [6, [2, 7]]]],
        [[4, [3, [4, 1]]], 8],
        [5, [[5, 1], 9]],
        [[3, [[2, 4], [3, 5]]], [3, [8, 6]]],
        [[[1, 9], [[4, 0], [8, 5]]], [[0, [1, 0]], [5, [8, 7]]]],
        [[[6, 6], [[5, 0], [3, 4]]], [[3, 7], 6]],
        [[[[0, 7], [6, 3]], [[2, 6], 8]], [[[3, 0], 8], [[4, 0], [6, 8]]]],
        [[[[0, 4], [6, 3]], [1, [9, 1]]], [[1, [1, 4]], 9]],
        [[[[8, 3], 2], [0, [6, 8]]], [5, [[4, 4], [1, 8]]]],
        [[[[1, 0], [7, 8]], 6], [3, [[5, 4], [4, 2]]]],
        [2, [9, 5]],
        [[4, [2, [0, 0]]], [[1, 3], [1, 9]]],
        [6, [[[2, 6], 2], 9]],
        [[6, [1, [7, 9]]], [[[7, 6], [8, 8]], [1, 7]]],
        [[[3, 7], [6, 9]], [5, 2]],
        [[[6, 1], 9], [[9, 7], [2, [9, 1]]]],
        [[[[2, 9], 7], [[8, 1], [2, 1]]], [4, [[3, 0], 9]]],
        [[[0, 0], [[8, 9], [2, 8]]], [[[8, 4], 5], [0, [1, 0]]]],
        [[[[6, 5], [3, 6]], [[6, 0], [0, 4]]], [[[4, 1], [4, 2]], [5, 1]]],
        [[[6, [2, 9]], [0, 7]], [8, [[7, 7], [9, 9]]]],
        [3, [[7, [5, 7]], [6, [9, 7]]]],
        [[0, [3, [9, 9]]], [[3, [5, 8]], [3, [6, 5]]]],
        [[[5, [7, 1]], [[9, 9], [7, 0]]], [0, 8]],
        [[[1, [4, 5]], [5, [4, 6]]], [1, [[1, 0], 9]]],
        [[[[4, 2], 7], [[0, 6], 7]], [8, [[6, 8], 0]]],
        [9, [3, [[7, 3], 9]]],
        [[7, 6], [[1, [2, 8]], [[3, 2], [9, 1]]]],
        [[[0, 5], [3, [6, 6]]], [[[1, 5], [1, 8]], [[8, 9], 8]]],
        [[8, [[1, 6], [2, 0]]], [[[3, 7], 3], 0]],
        [[[0, [6, 2]], [9, [5, 8]]], [[[1, 1], 4], [8, 4]]],
        [[[[3, 5], [5, 8]], 7], [[3, 6], 8]],
        [[5, [1, 0]], [[[1, 3], 6], [[6, 8], 5]]],
        [[[[7, 4], 0], [5, 1]], [[8, 7], 4]],
        [[3, [8, 3]], [[8, [3, 8]], 6]],
        [[1, [[0, 7], [2, 7]]], [[2, 9], [6, [8, 3]]]],
        [[[5, [1, 9]], [2, [7, 0]]], [[[5, 3], 2], [1, [9, 1]]]],
        [[[[0, 0], [0, 9]], [[0, 8], 4]], [[7, [3, 9]], 4]],
        [[4, 0], [0, 4]],
        [1, [[[5, 5], 4], [[7, 7], 3]]],
        [[[[0, 0], [9, 9]], [[9, 8], [8, 1]]], [[[1, 4], [0, 2]], [1, 0]]],
        [[[1, [4, 0]], 1], [4, [6, 5]]],
        [2, [[[3, 3], 4], [[2, 9], [3, 9]]]],
        [[[[3, 2], [2, 6]], [[5, 8], [1, 1]]], [[[4, 9], 9], 1]],
        [[[5, [1, 1]], 2], [[[2, 9], 3], [3, 4]]],
        [[[0, [6, 2]], [4, [3, 8]]], [[[3, 5], [6, 5]], [[9, 9], 2]]],
        [[[[1, 2], 5], [[5, 2], [3, 0]]], [[6, [0, 1]], [[3, 5], 8]]],
        [[2, [[5, 2], [5, 5]]], [3, [[1, 1], 2]]],
        [[[[4, 1], [8, 8]], [[2, 5], 2]], [[[1, 4], [3, 3]], 1]],
        [[[1, 1], [2, [3, 6]]], [[[0, 8], [3, 1]], [[1, 1], [2, 6]]]],
        [[0, [[5, 1], 5]], [1, [[0, 0], 7]]],
        [[[4, 1], [[2, 7], 4]], [[[8, 1], [2, 2]], [[3, 1], [1, 7]]]],
        [[[1, [7, 4]], [[1, 8], [7, 4]]], [[2, 3], [7, [9, 6]]]],
        [[[9, 6], [[6, 1], 5]], [[[9, 2], 3], [[2, 4], 8]]],
        [[[[8, 8], 2], 9], [5, 0]],
        [[[8, 5], [2, 1]], [8, [2, 9]]],
        [[[[5, 3], 9], 2], [[[1, 0], [2, 4]], 5]],
        [[[[0, 8], 0], 1], [[5, [4, 1]], [5, 2]]],
        [[[[6, 4], [6, 2]], [3, [4, 0]]], [[[9, 6], 8], [[6, 8], [5, 3]]]],
        [[9, 9], [1, 1]],
        [[0, [[9, 2], 1]], [[[6, 4], [8, 3]], 6]],
        [[[8, 9], [4, 3]], [[2, [2, 7]], [[2, 3], 8]]],
        [[[[8, 4], [7, 5]], [4, 2]], [[[9, 4], 0], [[9, 2], [7, 9]]]],
        [8, [[[6, 8], 3], [[5, 3], 5]]],
        [[[[9, 3], 0], [1, 4]], [[7, [4, 7]], 4]],
        [[[5, [4, 6]], 6], [[[8, 0], 1], [[1, 8], 0]]],
        [[[[0, 9], [1, 7]], [3, 9]], [[[2, 7], [5, 2]], [[4, 6], [7, 0]]]],
        [[[5, [0, 5]], 5], [[[8, 9], 2], [9, 6]]],
        [[6, [6, [9, 0]]], [[[7, 3], [5, 0]], [2, [1, 5]]]],
        [2, [[9, 6], [3, [3, 7]]]],
        [[[1, 6], [7, 1]], 9],
        [[[[2, 4], 2], [[6, 1], [6, 3]]], [[6, [9, 7]], 6]],
        [[[[6, 6], [2, 9]], [[9, 6], [3, 5]]], [5, 3]],
        [[[[7, 2], 6], 6], [3, [2, [8, 2]]]],
        [[[[6, 9], [6, 9]], 3], [[[6, 5], 4], 8]],
        [7, [[1, 8], [[2, 1], 5]]],
        [[9, 5], 9],
        [[[8, 9], [6, 4]], [[2, 2], [[3, 5], [9, 0]]]],
        [[[[2, 3], 8], [1, 8]], [[[8, 2], [3, 8]], [[0, 3], 2]]],
        [[0, [2, [1, 9]]], [9, 0]],
        [[[[7, 9], [0, 8]], 7], [5, [[3, 8], [0, 4]]]],
        [[[8, 9], [1, [6, 0]]], [[5, 3], 4]],
        [7, [[9, 9], 7]],
        [[[[6, 8], 2], [[4, 4], [4, 6]]], [[1, [4, 6]], [2, 7]]],
        [[6, 2], [5, [2, 1]]],
        [[[6, 0], [[0, 9], [8, 3]]], [7, [[1, 1], [0, 1]]]],
        [[[0, [0, 6]], [8, 0]], 0],
        [[3, [[4, 8], 5]], [[7, 3], [5, 0]]],
        [[6, [8, [0, 2]]], 2],
        [[[7, 2], 6], 3],
        [[[3, [1, 1]], 3], [[7, 9], [2, [2, 3]]]]
    ]

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
