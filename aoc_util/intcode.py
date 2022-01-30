class IntcodeError(Exception):
    pass


class IntcodeProgram:
    def __init__(self, start_list, input_values=1):
        # Dictionary for various opcodes
        self.instructions = {
            1: {
                'method': IntcodeProgram.addition,
                'params': 2,
                'overwrite': True,
                'consider_modes': True
            },
            2: {
                'method': IntcodeProgram.multiplication,
                'params': 2,
                'overwrite': True,
                'consider_modes': True
            },
            3: {
                'method': IntcodeProgram.get_input,
                'params': 1,
                'overwrite': False,
                'consider_modes': True
            },
            4: {
                'method': IntcodeProgram.store_output,
                'params': 1,
                'overwrite': False,
                'consider_modes': True
            },
            5: {
                'method': IntcodeProgram.jump_if_true,
                'params': 2,
                'overwrite': False,
                'consider_modes': True
            },
            6: {
                'method': IntcodeProgram.jump_if_false,
                'params': 2,
                'overwrite': False,
                'consider_modes': True
            },
            7: {
                'method': IntcodeProgram.less_than,
                'params': 2,
                'overwrite': True,
                'consider_modes': True
            },
            8: {
                'method': IntcodeProgram.equal_to,
                'params': 2,
                'overwrite': True,
                'consider_modes': True
            },
            9: {
                'method': IntcodeProgram.adjust_relative_base,
                'params': 1,
                'overwrite': False,
                'consider_modes': True
            }
        }

        # Initialize program
        if isinstance(start_list, str):
            self.program = list(map(int, start_list.split(',')))
        else:
            self.program = list(map(int, start_list))

        # Input methods
        self.input_values = input_values

        # Initial settings
        self.op_pos = 0
        self.rel_base = 0
        self.outputs = []

    def run(self):
        while self.read_values(num_values=1, consume=False)[0] != 99:
            # Get opcode
            op = self.read_values(1)[0]

            # Construct instruction payload
            instruction_payload = self.construct_payload(op)

            # Perform instruction
            self.instructions[op % 100]['method'](self, **instruction_payload)

    def read_values(self, num_values=1, consume=True):
        vals = self.program[self.op_pos: self.op_pos + num_values]
        if consume:
            self.op_pos += num_values
        return vals

    def construct_payload(self, opcode):
        # Read parameter values
        num_params = self.instructions[opcode % 100]['params']
        parameters = self.read_values(num_params)
        payload = {'params': parameters}

        # Consider modes (if required)
        if self.instructions[opcode % 100]['consider_modes']:
            param_modes = [(opcode % (1000 * 10 ** p)) // (100 * 10 ** p) for p in range(num_params)]

            # Adjust any parameters in relative mode
            while 2 in param_modes:
                param_index = param_modes.index(2)
                param_modes[param_index] = 0
                parameters[param_index] += self.rel_base

            # Extend memory if parameters point outside of current program
            for i, mode in enumerate(param_modes):
                if mode == 0 and parameters[i] >= len(self.program):
                    self.program.extend([0] * (parameters[i] - len(self.program) + 1))

            # Store in payload dictionary
            payload['modes'] = param_modes

        # Add destination address (if required)
        if self.instructions[opcode % 100]['overwrite']:
            dest_address = self.read_values(1)[0]
            # Slide if mode == 2
            if (opcode % (1000 * 10 ** num_params)) // (100 * 10 ** num_params) == 2:
                dest_address += self.rel_base

            # Extend memory if result needs to be stored outside of current program
            if dest_address >= len(self.program):
                self.program.extend([0] * (dest_address - len(self.program) + 1))

            # Store in payload dictionary
            payload['dest'] = dest_address

        return payload

    def addition(self, params, modes, dest):
        result = 0
        for i in range(len(modes)):
            result += params[i] if modes[i] == 1 else self.program[params[i]]
        self.program[dest] = result

    def multiplication(self, params, modes, dest):
        result = 1
        for i in range(len(modes)):
            result *= params[i] if modes[i] == 1 else self.program[params[i]]
        self.program[dest] = result

    def get_input(self, params, modes):
        if self.input_values is None:
            raise IntcodeError('Input instruction encountered without input method set.')

        if isinstance(self.input_values, int):
            self.program[params[0]] = self.input_values
        elif isinstance(self.input_values, list):
            self.program[params[0]] = self.input_values.pop(0)
        else:
            raise IntcodeError('Parameter input_values is neither an integer constant nor a list.')

    def store_output(self, params, modes):
        self.outputs.append(self.program[params[0]] if modes[0] == 0 else params[0])

    def jump_if_true(self, params, modes):
        if params[0] if modes[0] == 1 else self.program[params[0]]:
            self.op_pos = params[1] if modes[1] == 1 else self.program[params[1]]

    def jump_if_false(self, params, modes):
        if not (params[0] if modes[0] == 1 else self.program[params[0]]):
            self.op_pos = params[1] if modes[1] == 1 else self.program[params[1]]

    def less_than(self, params, modes, dest):
        left = params[0] if modes[0] == 1 else self.program[params[0]]
        right = params[1] if modes[1] == 1 else self.program[params[1]]

        if left < right:
            self.program[dest] = 1
        else:
            self.program[dest] = 0

    def equal_to(self, params, modes, dest):
        left = params[0] if modes[0] == 1 else self.program[params[0]]
        right = params[1] if modes[1] == 1 else self.program[params[1]]

        if left == right:
            self.program[dest] = 1
        else:
            self.program[dest] = 0

    def adjust_relative_base(self, params, modes):
        self.rel_base += params[0] if modes[0] == 1 else self.program[params[0]]

    def get_diagnostic_code(self):
        if any(self.outputs[:-1]):
            raise IntcodeError(f'Output contains non-zero value other than diagnostic value\n'
                               f'Outputs = {self.outputs}')
        return self.outputs[-1]

