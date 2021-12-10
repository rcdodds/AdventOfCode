from aocd.models import Puzzle
from aocd import get_data, submit
import pandas as pd
import numpy as np
import datetime
import json
import parse
import re


def split_input(input_str, cast_int, split_blanks):
    if split_blanks:
        delim = '\n\n'
    else:
        delim = '\n'

    if cast_int:
        return [int(s) for s in input_str.split(delim)]
    else:
        return input_str.split(delim)


def get_bag_dict(bag_str):
    outer_bag_dict = dict()
    for rule in bag_str:
        outer_bag = re.search(r'^(.*) bags contain', rule).group(1)
        outer_bag_dict[outer_bag] = [tup for tup in re.findall(r'(\d*) ([a-z]* [a-z]*) bags?(,|.)', rule)
                                     if not tup == ('', '')]

    # Let's take a look
    with open("sample.json", "w") as outfile:
        json.dump(outer_bag_dict, outfile, indent=4)

    return outer_bag_dict


def find_bag(bag_dict, bag_type):
    possible_outer_bags = []
    for outer in list(bag_dict.keys()):
        for inner_list in bag_dict[outer]:
            if bag_type in inner_list:
                possible_outer_bags.append(outer)
    return possible_outer_bags


def puzzle_a(input_a):
    outer_bag_dict = get_bag_dict(input_a)
    bags_to_search = ['shiny gold']     # Remaining bags to search for
    outer_bag_options = set()              # Results

    # Search for any bags of interest
    while bags_to_search:
        # Find any bags that can hold this type of bag
        immediate_outer_bags = find_bag(outer_bag_dict, bags_to_search[0])

        # Add the results to the list to be search
        bags_to_search.extend(immediate_outer_bags)

        # Add the results to the final answer
        outer_bag_options.update(immediate_outer_bags)

        # Remove the searched bag from the list to be searched
        bags_to_search.pop(0)

    return len(outer_bag_options)


def puzzle_b(input_b, top_bag):
    dict_of_bags = get_bag_dict(input_b)
    count = 0

    for bag in dict_of_bags[top_bag]:
        if bag[0] != '':
            bag_qt = int(bag[0])
            count += bag_qt

            bags_inside_current = puzzle_b(input_b, bag[1])
            count += (bag_qt * bags_inside_current)

    return count


if __name__ == '__main__':
    # Set puzzle of interest
    year = 2020
    day = 7

    # Get puzzle inputs
    puzzle = Puzzle(year=year, day=day)
    puzzle_input = split_input(get_data(year=year, day=day, block=True), cast_int=False, split_blanks=False)

    # Solve puzzles
    puzzle_a_result = puzzle_a(puzzle_input)
    puzzle_b_result = puzzle_b(puzzle_input, 'shiny gold')

    ready = True
    print('Guess for puzzle A: ' + str(puzzle_a_result))
    print('Guess for puzzle B: ' + str(puzzle_b_result))
    if ready:
        # Attempt to submit guess for puzzle A
        if not puzzle.answered_a and puzzle_a_result != 0:
            if puzzle_a_result not in puzzle.incorrect_answers_a.values():
                submit(puzzle_a_result, part='a', year=year, day=day)
            else:
                print('Guess for puzzle A was previously attempted: {}'.format(puzzle_a_result))

        # Attempt to submit guess for puzzle B
        if not puzzle.answered_b and puzzle_b_result != 0:
            if puzzle_b_result not in puzzle.incorrect_answers_b.values():
                submit(puzzle_b_result, part='b', year=year, day=day)
            else:
                print('Guess for puzzle B was previously attempted: {}'.format(puzzle_b_result))
