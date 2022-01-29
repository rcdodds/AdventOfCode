import unittest
from intcode import IntcodeProgram


class IntcodeTester(unittest.TestCase):
    def test_day02_01(self):
        icp = IntcodeProgram([1, 0, 0, 0, 99])
        icp.run()
        self.assertEqual([2, 0, 0, 0, 99], icp.program)

    def test_day02_02(self):
        icp = IntcodeProgram([2, 3, 0, 3, 99])
        icp.run()
        self.assertEqual([2, 3, 0, 6, 99], icp.program)

    def test_day02_03(self):
        icp = IntcodeProgram([2, 4, 4, 5, 99, 0])
        icp.run()
        self.assertEqual([2, 4, 4, 5, 99, 9801], icp.program)

    def test_day02_04(self):
        icp = IntcodeProgram([1, 1, 1, 4, 99, 5, 6, 0, 99])
        icp.run()
        self.assertEqual([30, 1, 1, 4, 2, 5, 6, 0, 99], icp.program)

    def test_day02_real(self):
        real_input = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 6, 1, 19, 1, 5, 19, 23, 1, 13, 23, 27, 1, 6,
                      27, 31, 2, 31, 13, 35, 1, 9, 35, 39, 2, 39, 13, 43, 1, 43, 10, 47, 1, 47, 13, 51, 2, 13, 51, 55,
                      1, 55, 9, 59, 1, 59, 5, 63, 1, 6, 63, 67, 1, 13, 67, 71, 2, 71, 10, 75, 1, 6, 75, 79, 1, 79, 10,
                      83, 1, 5, 83, 87, 2, 10, 87, 91, 1, 6, 91, 95, 1, 9, 95, 99, 1, 99, 9, 103, 2, 103, 10, 107, 1, 5,
                      107, 111, 1, 9, 111, 115, 2, 13, 115, 119, 1, 119, 10, 123, 1, 123, 10, 127, 2, 127, 10, 131, 1,
                      5, 131, 135, 1, 10, 135, 139, 1, 139, 2, 143, 1, 6, 143, 0, 99, 2, 14, 0, 0]
        real_input[1] = 12
        real_input[2] = 2
        icp = IntcodeProgram(real_input)
        icp.run()
        self.assertEqual(5290681, icp.program[0])

    def test_day05_multiply_immediate(self):
        icp = IntcodeProgram([1002, 4, 3, 4, 33])
        icp.run()
        self.assertEqual([1002, 4, 3, 4, 99], icp.program)

    def test_day05_add_immediate(self):
        icp = IntcodeProgram([1101, 100, -1, 4, 0])
        icp.run()
        self.assertEqual([1101, 100, -1, 4, 99], icp.program)

    def test_day05_real(self):
        real_input = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1101, 90, 64, 225, 1101, 15, 56, 225, 1, 14, 153,
                      224, 101, -147, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 3, 224, 1, 224, 223, 223, 2, 162,
                      188, 224, 101, -2014, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 6, 224, 224, 1, 223, 224, 223,
                      1001, 18, 81, 224, 1001, 224, -137, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 3, 224, 1, 223,
                      224, 223, 1102, 16, 16, 224, 101, -256, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 6, 224, 1,
                      223, 224, 223, 101, 48, 217, 224, 1001, 224, -125, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 3,
                      224, 1, 224, 223, 223, 1002, 158, 22, 224, 1001, 224, -1540, 224, 4, 224, 1002, 223, 8, 223, 101,
                      2, 224, 224, 1, 223, 224, 223, 1101, 83, 31, 225, 1101, 56, 70, 225, 1101, 13, 38, 225, 102, 36,
                      192, 224, 1001, 224, -3312, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 4, 224, 1, 224, 223, 223,
                      1102, 75, 53, 225, 1101, 14, 92, 225, 1101, 7, 66, 224, 101, -73, 224, 224, 4, 224, 102, 8, 223,
                      223, 101, 3, 224, 224, 1, 224, 223, 223, 1101, 77, 60, 225, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0,
                      256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227,
                      274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0,
                      1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105,
                      1, 99999, 7, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 329, 1001, 223, 1, 223, 1007, 226, 677,
                      224, 1002, 223, 2, 223, 1005, 224, 344, 101, 1, 223, 223, 108, 226, 226, 224, 1002, 223, 2, 223,
                      1006, 224, 359, 101, 1, 223, 223, 7, 226, 226, 224, 102, 2, 223, 223, 1005, 224, 374, 101, 1, 223,
                      223, 8, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 389, 1001, 223, 1, 223, 107, 677, 677, 224,
                      102, 2, 223, 223, 1006, 224, 404, 101, 1, 223, 223, 1107, 677, 226, 224, 102, 2, 223, 223, 1006,
                      224, 419, 1001, 223, 1, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 434, 1001, 223, 1,
                      223, 7, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 449, 1001, 223, 1, 223, 1107, 226, 226, 224,
                      1002, 223, 2, 223, 1005, 224, 464, 101, 1, 223, 223, 1108, 226, 677, 224, 102, 2, 223, 223, 1005,
                      224, 479, 101, 1, 223, 223, 1007, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 494, 1001, 223, 1,
                      223, 1107, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 509, 101, 1, 223, 223, 1007, 226, 226,
                      224, 1002, 223, 2, 223, 1006, 224, 524, 101, 1, 223, 223, 107, 226, 226, 224, 1002, 223, 2, 223,
                      1005, 224, 539, 1001, 223, 1, 223, 1108, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 554, 101, 1,
                      223, 223, 1008, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 569, 1001, 223, 1, 223, 8, 226, 677,
                      224, 102, 2, 223, 223, 1005, 224, 584, 1001, 223, 1, 223, 1008, 677, 677, 224, 1002, 223, 2, 223,
                      1006, 224, 599, 1001, 223, 1, 223, 108, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 614, 1001,
                      223, 1, 223, 108, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 629, 101, 1, 223, 223, 8, 677, 226,
                      224, 102, 2, 223, 223, 1005, 224, 644, 101, 1, 223, 223, 107, 677, 226, 224, 1002, 223, 2, 223,
                      1005, 224, 659, 101, 1, 223, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 674, 1001,
                      223, 1, 223, 4, 223, 99, 226]
        icp = IntcodeProgram(real_input, input_values=1)
        icp.run()
        self.assertEqual(7988899, icp.get_diagnostic_code())

        icp2 = IntcodeProgram(real_input, input_values=5)
        icp2.run()
        self.assertEqual(13758663, icp2.get_diagnostic_code())

    def test_day05_input_equal_to_8_position(self):
        icp = IntcodeProgram([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], input_values=8)
        icp.run()
        self.assertEqual(1, icp.get_diagnostic_code())

        icp2 = IntcodeProgram([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], input_values=7)
        icp2.run()
        self.assertEqual(0, icp2.get_diagnostic_code())

    def test_day05_input_less_than_8_position(self):
        icp = IntcodeProgram([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], input_values=6)
        icp.run()
        self.assertEqual(1, icp.get_diagnostic_code())

        icp2 = IntcodeProgram([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], input_values=8)
        icp2.run()
        self.assertEqual(0, icp2.get_diagnostic_code())

    def test_day05_input_equal_to_8_immediate(self):
        icp = IntcodeProgram([3, 3, 1108, -1, 8, 3, 4, 3, 99], input_values=8)
        icp.run()
        self.assertEqual(1, icp.get_diagnostic_code())

        icp2 = IntcodeProgram([3, 3, 1108, -1, 8, 3, 4, 3, 99], input_values=88)
        icp2.run()
        self.assertEqual(0, icp2.get_diagnostic_code())

    def test_day05_input_less_than_8_immediate(self):
        icp = IntcodeProgram([3, 3, 1107, -1, 8, 3, 4, 3, 99], input_values=6)
        icp.run()
        self.assertEqual(1, icp.get_diagnostic_code())

        icp2 = IntcodeProgram([3, 3, 1107, -1, 8, 3, 4, 3, 99], input_values=8)
        icp2.run()
        self.assertEqual(0, icp2.get_diagnostic_code())

    def test_day05_input0_position_jumps(self):
        icp = IntcodeProgram([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], input_values=6)
        icp.run()
        self.assertEqual(1, icp.get_diagnostic_code())

        icp2 = IntcodeProgram([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], input_values=0)
        icp2.run()
        self.assertEqual(0, icp2.get_diagnostic_code())

    def test_day05_input0_immediate_jumps(self):
        icp = IntcodeProgram([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], input_values=6)
        icp.run()
        self.assertEqual(1, icp.get_diagnostic_code())

        icp2 = IntcodeProgram([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], input_values=0)
        icp2.run()
        self.assertEqual(0, icp2.get_diagnostic_code())

    def test_day05_large_jumps_and_equality(self):
        icp = IntcodeProgram([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                              1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                              999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], input_values=7)
        icp.run()
        self.assertEqual(999, icp.get_diagnostic_code())

        icp2 = IntcodeProgram([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                               1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                               999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], input_values=8)
        icp2.run()
        self.assertEqual(1000, icp2.get_diagnostic_code())

        icp3 = IntcodeProgram([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                               1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                               999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], input_values=9)
        icp3.run()
        self.assertEqual(1001, icp3.get_diagnostic_code())

    def test_day07_amp_settings(self):
        icp_inputs = [
            [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
            [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
             101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0],
            [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
             1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
        ]
        amp_settings = [[4, 3, 2, 1, 0], [0, 1, 2, 3, 4], [1, 0, 4, 3, 2]]
        results = [43210, 54321, 65210]

        for x in range(3):
            prior_output = 0
            while amp_settings[x]:
                icp = IntcodeProgram(icp_inputs[x], input_values=[amp_settings[x].pop(0), prior_output])
                icp.run()
                prior_output = icp.get_diagnostic_code()
            self.assertEqual(results[x], prior_output)


if __name__ == '__main__':
    unittest.main()
