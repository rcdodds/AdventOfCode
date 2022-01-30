# Libraries
import logging
from aocd.models import Puzzle
from aocd import submit

logging.basicConfig(level=logging.WARNING)


class ImageLayer:
    def __init__(self, pixels):
        self.pixels = pixels

    def get_pixel_counts(self, digit):
        return self.pixels.count(digit)


def solve_part_a(part_a_input):
    image, width, height, lowest_zero_count = list(map(int, list(part_a_input))), 25, 6, None
    image_layers = []

    # Create image
    while image:
        image_layers.append(ImageLayer([image.pop(0) for _ in range(width * height)]))

    zero_counts = [x.get_pixel_counts(0) for x in image_layers]
    layer_num = zero_counts.index(min(zero_counts))
    return image_layers[layer_num].get_pixel_counts(1) * image_layers[layer_num].get_pixel_counts(2)


def solve_part_b(part_b_input):
    image, width, height, image_layers = list(map(int, list(part_b_input))), 25, 6, []

    # Create image
    while image:
        image_layers.append(ImageLayer([image.pop(0) for _ in range(width * height)]))

    # Find actual value for each position
    actual_image = []
    for i in range(len(image_layers[0].pixels)):
        val, layer = 2, 0
        while val == 2:
            val = image_layers[layer].pixels[i]
            layer += 1
        actual_image.append(val)

    for x in range(height):
        print(actual_image[width * x: width * x + 25])      # For my input > YGRYZ


if __name__ == '__main__':
    # Puzzle info
    use_test_data, backtest = (False, True)
    (year, day) = (2019, 8)
    pzl = Puzzle(year=year, day=day)
    pzl_dict = {'A': {'solved': pzl.answered_a, 'solve_func': solve_part_a,
                      'answer': pzl.answer_a if pzl.answered_a else None},
                'B': {'solved': pzl.answered_b, 'solve_func': solve_part_b,
                      'answer': pzl.answer_b if pzl.answered_b else None}}

    # Test inputs
    test_data = '123456789012'

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
