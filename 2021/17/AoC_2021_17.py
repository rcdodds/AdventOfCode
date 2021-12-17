# Libraries
import numpy as np
from aocd.models import Puzzle
from aocd import submit

# TARGET RANGE
min_x = 257
max_x = 286
min_y = -101
max_y = -57
# min_x = 20
# max_x = 30
# min_y = -10
# max_y = -5


class LaunchedProbe:
    def __init__(self, v_x, v_y):
        self.x, self.y = (0, 0)
        self.x_velocity, self.y_velocity = (v_x, v_y)
        self.steps = 0
        self.max_height = 0

    def move_step(self):
        # Update position
        self.x += self.x_velocity
        self.y += self.y_velocity

        # Update velocities for next step
        self.x_velocity = (self.x_velocity - 1) if self.x_velocity > 0\
            else (self.x_velocity + 1) if self.x_velocity < 0 else 0
        self.y_velocity -= 1

        # Update max height if relevant
        if self.y > self.max_height:
            self.max_height = self.y


def solve_puzzle(letter):
    # Consider a bunch of velocities
    max_heights = []
    for x in range(0, 1000, 1):
        for y in range(-500, 500, 1):
            # Create probe
            probe = LaunchedProbe(x, y)

            # Assume success
            hit_target = True

            # Map out steps until the target range is hit OR has been conclusively missed
            while not (min_x <= probe.x <= max_x) or not (min_y <= probe.y <= max_y):
                # Move one step
                probe.move_step()

                # Determine if range has been missed
                if probe.x < min_x and probe.x_velocity == 0:
                    # Probe did not make it far enough right (x-velocity not enough)
                    hit_target = False
                    break
                elif probe.x > max_x:
                    # Probe went too far right
                    hit_target = False
                    break
                elif probe.y < min_y and probe.y_velocity <= 0:
                    # Probe did not make it high enough (y-velocity not enough)
                    hit_target = False
                    break

            if hit_target:
                print(f'HIT - ({x}, {y}) >> max_height = {probe.max_height}')
                max_heights.append(probe.max_height)
            else:
                print(f'MISS - ({x}, {y})')

    if letter == 'A':
        return max(max_heights)
    elif letter == 'B':
        return len(max_heights)


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 17)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Consider both puzzles
    for part in ['A', 'B']:
        if not puzzle_solution[part]['solved']:
            # Attempt solution
            guess = solve_puzzle(part)
            puzzle_solution[part]['guess'] = guess
            print('Guess for puzzle {}: {}'.format(part, guess))

            # Submit if ready
            if ready_to_solve and guess != 0:
                submit(guess, part=part, year=year, day=day)
