from aocd.models import Puzzle
from aocd import submit


class InvalidPuzzleTypeError(Exception):
    """Raised when trying to work with a puzzle type that doesn't exist"""
    pass


def play_round_naive(previous_numbers):
    # Reverse list to deal with most recent occurrences
    previous_numbers.reverse()

    # Extract the most recent number
    last_number_spoken = previous_numbers[0]

    # Attempt to find the most recent occurrence
    try:
        most_recent_occurrence = previous_numbers[1:].index(last_number_spoken) + 1
        next_number = most_recent_occurrence
    except ValueError:
        next_number = 0

    # Clean up
    previous_numbers.reverse()

    return next_number


def solve_puzzle(pzl_data, letter):
    if letter == 'A':
        number_list = pzl_data[:]
        while len(number_list) < 2020:
            number_list.append(play_round_naive(number_list))
            print('Numbers Spoken = {}'.format(len(number_list)))
        return number_list[-1]

    elif letter == 'B':
        earliest_rounds = {}
        latest_rounds = {number: pzl_data.index(number) + 1 for number in pzl_data}
        latest_round = len(pzl_data)
        new_num = pzl_data[-1]
        while latest_round < 30000000:
            # Play a round
            latest_number = new_num
            earlier_round = earliest_rounds.get(latest_number, 0)
            new_num = latest_round - earlier_round if earlier_round else 0
            latest_round += 1

            # Log round in dictionaries
            new_earliest = latest_rounds.get(new_num)
            latest_rounds[new_num] = latest_round
            if new_earliest:
                earliest_rounds[new_num] = new_earliest
        return new_num

    else:
        # Invalid letter submitted
        print('Gasp! You tried to use a puzzle type that does not exist.')
        raise InvalidPuzzleTypeError


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2020, 15)
    puzzle = Puzzle(year=year, day=day)
    puzzle_data = puzzle.input_data
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0},
                       'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = False

    # Format puzzle input
    puzzle_data = [int(x) for x in puzzle_data.split(',')]
    # puzzle_data = [0, 3, 6]
    # puzzle_data = [int(puzzle_string) for puzzle_string in puzzle_data]

    # Consider both puzzles
    for part in ['A', 'B']:
        # If puzzle is not already solved...
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(puzzle_data, part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess:
                submit(guess, part=part, year=year, day=day)
