# Libraries
from aocd.models import Puzzle
from aocd import submit
import itertools

rules = {}


def parse_rules(rule_strings, overwrite_8_11=False):
    rule_dict, letter_rules = {}, set()

    # Construct original dictionary of all rules and set of the rules for specific letters
    for rule_str in rule_strings.split('\n'):
        rule_pieces = rule_str.split(': ')
        if rule_pieces[1].find('\"') != -1:
            rule_dict[int(rule_pieces[0])] = rule_pieces[1].split('\"')[1]
            letter_rules.add(int(rule_pieces[0]))
        else:
            rule_dict[int(rule_pieces[0])] = [list(map(int, x.split(' '))) for x in rule_pieces[1].split(' | ')]

    if overwrite_8_11:
        rule_dict[8] = [[42], [42, 8]]
        rule_dict[11] = [[42, 31], [42, 11, 31]]

    return rule_dict


def find_options(start):
    # Reached the "bottom" rule with an actual letter
    if isinstance(rules[start], str):
        return rules[start]
    else:
        options = set()
        for option in rules[start]:
            new_options = []
            for next_rule in option:
                if not new_options:
                    new_options = find_options(next_rule)
                else:
                    new_options = [''.join(o) for o in itertools.product(new_options, find_options(next_rule))]
            options.update(new_options)
        return options


def solve_part_a(puzzle_input):
    global rules
    rules = parse_rules(puzzle_input.split('\n\n')[0])
    valid_options = find_options(0)
    return len(valid_options.intersection(set(puzzle_input.split('\n\n')[1].split('\n'))))


def solve_part_b(puzzle_input):
    global rules
    rules = parse_rules(puzzle_input.split('\n\n')[0], overwrite_8_11=True)

    # Rule 0 is rule 8 + rule 11.
    # Rule 8 is now one or more matches to rule 42.
    # Rule 11 is an even number of matches to rule 42 then rule 31.
    rule_42, rule_31 = find_options(42), find_options(31)
    assert max(map(len, rule_42)) == min(map(len, rule_42))
    assert max(map(len, rule_31)) == min(map(len, rule_31))
    assert max(map(len, rule_42)) == min(map(len, rule_31))
    group_length = max(map(len, rule_42))

    # Evaluate each input line individually
    matches = set()
    for input_line in puzzle_input.split('\n\n')[1].split('\n'):
        valid, current_group, groups_42, groups_31 = True, 1, 0, 0
        while valid and current_group * group_length <= len(input_line):
            group = input_line[(current_group-1)*group_length: current_group*group_length]
            current_group += 1

            # Check validity of group
            if group in rule_42 and not groups_31:
                groups_42 += 1
            elif group in rule_31:
                groups_31 += 1
            else:
                valid = False

        if valid and (groups_31 >= groups_42 or not groups_31):
            valid = False

        if valid:
            matches.add(input_line)

    return len(matches)


if __name__ == '__main__':
    # Puzzle info
    test, solve, backtest = (False, True, True)
    (year, day) = (2020, 19)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a if not backtest else False,
                      'answer': pzl.answer_a if pzl.answered_a else None,
                      'solve_func': solve_part_a},
                'B': {'solved': pzl.answered_b if not backtest else False,
                      'answer': pzl.answer_b if pzl.answered_b else None,
                      'solve_func': solve_part_b}}

    # Test inputs
    test_data = '0: 4 1 5\n1: 2 3 | 3 2\n2: 4 4 | 5 5\n3: 4 5 | 5 4\n4: "a"\n5: ' \
                '"b"\n\nababbb\nbababa\nabbbab\naaabbb\naaaabbb '
    test_data = '42: 9 14 | 10 1\n9: 14 27 | 1 26\n10: 23 14 | 28 1\n1: "a"\n11: 42 31\n5: 1 14 | 15 1\n19: 14 1 | 14 ' \
                '14\n12: 24 14 | 19 1\n16: 15 1 | 14 14\n31: 14 17 | 1 13\n6: 14 14 | 1 14\n2: 1 24 | 14 4\n0: 8 ' \
                '11\n13: 14 3 | 1 12\n15: 1 | 14\n17: 14 2 | 1 7\n23: 25 1 | 22 14\n28: 16 1\n4: 1 1\n20: 14 14 | 1 ' \
                '15\n3: 5 14 | 16 1\n27: 1 6 | 14 18\n14: "b"\n21: 14 1 | 1 14\n25: 1 1 | 1 14\n22: 14 14\n8: 42\n26: ' \
                '14 22 | 1 20\n18: 15 15\n7: 14 5 | 1 21\n24: 14 ' \
                '1\n\nabbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa\nbbabbbbaabaabba\nbabbbbaabbbbbabbbbbbaabaaabaaa' \
                '\naaabbbbbbaaaabaababaabababbabaaabbababababaaa\nbbbbbbbaaaabbbbaaabbabaaa' \
                '\nbbbababbbbaaaaaaaabbababaaababaabab\nababaaaaaabaaab\nababaaaaabbbaba\nbaabbaaaabbaaaababbaababb' \
                '\nabbbbabbbbaaaababbbbbbaaaababb\naaaaabbaabaaaaababaa\naaaabbaaaabbaaa' \
                '\naaaabbaabbaaaaaaabbbabbbaaabbaabaaa\nbabaaabbbaaabaababbaabababaaab' \
                '\naabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba '

    # Consider both puzzles
    for part in pzl_dict.keys():
        if pzl_dict[part]['solved'] and not backtest:
            print(f'Year {year} Day {day} Part {part} already solved with answer = {pzl_dict[part]["answer"]}')
        else:
            # Attempt solution
            pzl_dict[part]['answer'] = pzl_dict[part]['solve_func'](pzl.input_data if not test else test_data)
            print(f'Year {year} Day {day} Part {part} answer = {pzl_dict[part]["answer"]}')

            # Submit if ready
            if solve and pzl_dict[part]['answer']:
                submit(pzl_dict[part]['answer'], part=part, year=year, day=day)
