# Libraries
from aocd.models import Puzzle
from aocd import submit
from copy import deepcopy

# Global variables
move_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
room_dests = {'A': 2, 'B': 4, 'C': 6, 'D': 8}


class Board:
    def __init__(self, stack_dict, hallway=None, cost=None):
        self.rooms = stack_dict
        self.hallway = hallway if hallway else [None for _ in range(11)]
        self.cost = cost if cost else 0

    def __repr__(self):
        return repr((self.hallway, self.rooms, self.cost))

    def flatten_to_tuple(self):
        return tuple(tuple(x) for x in self.rooms.values()) + tuple(self.hallway)


def find_all_valid_moves(current_board):
    next_states = []

    # Determine what can be moved from the hallway into a stack
    for spot, value in enumerate(current_board.hallway):
        # Only consider spots with values where the destination stack isn't "contaminated"
        if value and all(dest_letter == value for dest_letter in current_board.rooms[value]):
            # Ensure path to the correct room is clear
            if not any(current_board.hallway[min(spot + 1, room_dests[value]): max(spot - 1, room_dests[value]) + 1]):
                new_hallway = deepcopy(current_board.hallway)
                new_hallway[spot] = None  # Remove letter from hallway
                new_rooms = deepcopy(current_board.rooms)
                new_rooms[value].append(value)  # Add letter to room
                distance_traveled = abs(spot - room_dests[value]) + (4 - len(current_board.rooms[value]))
                new_cost = current_board.cost + (distance_traveled * move_costs[value])  # Add cost
                next_states.append(Board(new_rooms, new_hallway, new_cost))     # Add new state to possibilities

    # Any top value in an incorrect room can be moved to any reachable hallway spot
    for room in current_board.rooms.keys():
        # Only consider rooms that are still "contaminated"
        if not all(dest_letter == room for dest_letter in current_board.rooms[room]):
            # Progress as far as possible down the hallway in both the left (-1) and right (+1)
            for dir in [-1, 1]:
                # Take one step into hallway to initialize search
                spot = room_dests[room]
                while 0 <= spot <= len(current_board.hallway) - 1 and current_board.hallway[spot] is None:
                    # Cannot stop on spots outside of rooms
                    if spot not in room_dests.values():
                        new_hallway = deepcopy(current_board.hallway)
                        new_hallway[spot] = current_board.rooms[room][-1]     # Add letter to hallway
                        new_rooms = deepcopy(current_board.rooms)
                        moved_letter = new_rooms[room].pop()  # Remove letter from room
                        distance_traveled = abs(spot - room_dests[room]) + (5 - len(current_board.rooms[room]))
                        new_cost = current_board.cost + (distance_traveled * move_costs[moved_letter])  # Add cost
                        next_state = Board(new_rooms, new_hallway, new_cost)
                        next_states.append(next_state)     # Add new state to possibilities

                    # Move spot down hallway
                    spot += dir
    return next_states


def combine_same_boards(boards):
    unique_boards = {}
    for board in boards:
        board_only_tuple = board.flatten_to_tuple()
        if board_only_tuple in unique_boards.keys():
            if unique_boards[board_only_tuple].cost > board.cost:
                unique_boards[board_only_tuple].cost = board.cost
        else:
            unique_boards[board_only_tuple] = board
    return unique_boards.values()


def solve_puzzle_part_b():
    input_dict = {'A': ['C', 'D', 'D', 'B'], 'B': ['D', 'B', 'C', 'C'], 'C': ['D', 'A', 'B', 'A'], 'D': ['A', 'C', 'A', 'B']}     # Real input
    start_board = Board(input_dict)
    reachable_states = [start_board]
    done_costs = set()
    rounds = 1

    # For each known state, add the states that can be reached with a valid move
    while reachable_states:
        print(f'Playing round {rounds}')
        rounds += 1

        next_reachable_states = []
        for current_state in reachable_states:
            # If this state is a completed solution, store the cost
            if current_state.rooms == {letter: [letter] * 4 for letter in 'ABCD'}:
                done_costs.add(current_state.cost)
            # Otherwise, find all next possible states
            else:
                next_reachable_states.extend(find_all_valid_moves(current_state))

        # Combine boards with the same rooms / hallways and restart
        reachable_states = combine_same_boards(next_reachable_states)
    return min(done_costs)


if __name__ == '__main__':
    # Get & format puzzle data
    (year, day) = (2021, 23)
    puzzle = Puzzle(year=year, day=day)

    # Solve a part of the puzzle if necessary
    if not puzzle.answered_a:
        submit(14350, part='A', year=year, day=day)  # Solved by hand today
    elif not puzzle.answered_b:
        submit(solve_puzzle_part_b(), part='B', year=year, day=day)
    else:
        print(f'Puzzle for year {year} // day {day} already solved!\n'
              f'Answer for part A = {puzzle.answer_a}\n'
              f'Answer for part B = {puzzle.answer_b}')
