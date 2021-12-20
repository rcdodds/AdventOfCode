# Libraries
import re
import numpy as np
from aocd.models import Puzzle
from aocd import submit

hex_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']


def hex_to_bin(hex_str):
    binary_bits = [bin(hex_chars.index(hex_ch))[2:].zfill(4) for hex_ch in hex_str]
    return ''.join(binary_bits)


def bin_to_hex(bin_str):
    chunk_size = 4
    hex_bits = [hex_chars[int(bin_str[i:i+chunk_size], 2)] for i in range(0, len(bin_str), chunk_size)]
    return ''.join(hex_bits)


def bin_to_dec(bin_s):
    return int(bin_s, 2)


def parse_packet(remaining_packet_string):
    # Extracting version / type
    header_info = tuple(map(bin_to_dec, re.match(r'^([0-1]{3})([0-1]{3})', remaining_packet_string).groups()))
    version_sum = header_info[0]
    read_chars = 6

    # Literal Packet
    if header_info[1] == 4:
        literal_value_binary = []
        while True:
            # Extract next group
            literal_group_bits = re.match(r'^([0-1])([0-1]{4})', remaining_packet_string[read_chars:]).groups()
            read_chars += 5

            # Store group in output
            literal_value_binary.append(literal_group_bits[1])

            # Last group found
            if literal_group_bits[0] == '0':
                # Find literal value
                packet_value = bin_to_dec(''.join(literal_value_binary))
                break

    # Operator Packet
    else:
        # Extract length type
        length_type_regex = r'(?:^(0)([0-1]{15}))|(?:^(1)([0-1]{11}))'
        length_type = re.match(length_type_regex, remaining_packet_string[read_chars:]).groups()
        length_type = tuple(val for val in length_type if val)
        read_chars += sum(map(len, length_type))

        # Initialize list for sub-packet values
        sub_packet_values = []

        # Sub-packets will be restricted by total length
        if length_type[0] == '0':
            sub_packet_length = bin_to_dec(length_type[1])
            previously_read_chars = read_chars
            while read_chars - previously_read_chars < sub_packet_length:
                vsn, rc, pack_val = parse_packet(remaining_packet_string[read_chars:])
                version_sum += vsn
                read_chars += rc
                sub_packet_values.append(pack_val)

        # Sub-packets will be restricted by total count
        else:
            sub_packet_count = bin_to_dec(length_type[1])

            # Parse that number of packets
            for _ in range(sub_packet_count):
                vsn, rc, pack_val = parse_packet(remaining_packet_string[read_chars:])
                version_sum += vsn
                read_chars += rc
                sub_packet_values.append(pack_val)

        # Decipher various type IDs
        if header_info[1] == 0:
            packet_value = sum(sub_packet_values)
        elif header_info[1] == 1:
            packet_value = np.prod(sub_packet_values, dtype=np.int64)
        elif header_info[1] == 2:
            packet_value = min(sub_packet_values)
        elif header_info[1] == 3:
            packet_value = max(sub_packet_values)
        elif header_info[1] == 5:
            packet_value = 1 if sub_packet_values[0] > sub_packet_values[1] else 0
        elif header_info[1] == 6:
            packet_value = 1 if sub_packet_values[0] < sub_packet_values[1] else 0
        elif header_info[1] == 7:
            packet_value = 1 if sub_packet_values[0] == sub_packet_values[1] else 0
        else:
            raise Exception

    return version_sum, read_chars, packet_value


def solve_puzzle(pzl_data, letter):
    if letter == 'A':
        return parse_packet(hex_to_bin(pzl_data))[0]
    elif letter == 'B':
        return parse_packet(hex_to_bin(pzl_data))[2]


if __name__ == '__main__':
    # Puzzle info
    (year, day) = (2021, 16)
    puzzle = Puzzle(year=year, day=day)
    puzzle_solution = {'A': {'solved': puzzle.answered_a, 'guess': 0}, 'B': {'solved': puzzle.answered_b, 'guess': 0}}
    ready_to_solve = True

    # Format puzzle tree_input
    puzzle_data = puzzle.input_data

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
