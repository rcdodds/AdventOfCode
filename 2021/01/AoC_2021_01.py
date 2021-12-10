import pandas as pd
import numpy as np
from aocd.models import Puzzle


def count_increases(input_list):
    # Define df
    df = pd.DataFrame()
    df['input_values'] = input_list

    # Add delta column
    df['delta'] = df['input_values'].diff()

    # Add change direction column
    df['change_direction'] = np.where(df['delta'] > 0, 'increase', np.where(df['delta'] < 0, 'decrease', 'no change'))

    # Show results
    return df['change_direction'].value_counts()['increase']


def puzzle_a(input_a):
    solution_a = count_increases(input_a)
    print('Solution for puzzle A: ' + str(solution_a))


def puzzle_b(input_b):
    solution_b = count_increases(input_b)
    print('Solution for puzzle B: ' + str(solution_b))


if __name__ == '__main__':
    # Pull AoC puzzle
    puzzle = Puzzle(year=2021, day=1)

    # Prepare data frame
    input_data_a = list(map(int, puzzle.input_data.split('\n')))
    puzzle_a(input_data_a)

    input_data_b = pd.Series(input_data_a).rolling(3).sum()
    puzzle_b(input_data_b)

