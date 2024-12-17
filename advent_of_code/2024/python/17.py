import re
from dataclasses import dataclass


@dataclass
class Registers:
    A: int
    B: int
    C: int


def combo_operand(operand, registers):
    assert 0 <= operand <= 7
    if operand <= 3:
        return operand
    if operand == 4:
        return registers.A
    if operand == 5:
        return registers.B
    if operand == 6:
        return registers.C
    if operand == 7:
        raise ValueError('operand 7 not supported')


def run_program(program, registers):
    program = program.copy()
    pointer = 0
    output = []
    while pointer < len(program):
        opcode, operand = program[pointer], program[pointer + 1]

        if opcode == 0:
            registers.A = registers.A // 2 ** combo_operand(operand, registers)
            pointer += 2
        elif opcode == 1:
            registers.B = registers.B ^ operand
            pointer += 2
        elif opcode == 2:
            registers.B = combo_operand(operand, registers) % 8
            pointer += 2
        elif opcode == 3:
            if registers.A != 0:
                pointer = operand
            else:
                pointer += 2
        elif opcode == 4:
            registers.B = registers.B ^ registers.C
            pointer += 2
        elif opcode == 5:
            output.append(combo_operand(operand, registers) % 8)
            pointer += 2
        elif opcode == 6:
            registers.B = registers.A // 2 ** combo_operand(operand, registers)
            pointer += 2
        elif opcode == 7:
            registers.C = registers.A // 2 ** combo_operand(operand, registers)
            pointer += 2
    return ','.join(map(str, output))


# 2,4,     B = A % 8
# 1,5,     B = B ^ 5
# 7,5,     C = A // 2 ** B
# 1,6,     B = B ^ 6
# 0,3,     A = A // 2 ** 3
# 4,3,     B = B ^ C
# 5,5,     output.append(B % 8)
# 3,0      repeat until A == 0


def run_simplified_program(A):
    B, C = 0, 0
    output = []
    while A != 0:
        B = A % 8
        B = B ^ 5
        C = A // 2**B
        B = B ^ 6
        A = A // 2**3
        B = B ^ C
        output.append(B % 8)
    return output


def run_more_simplified_program(A):
    output = []
    while A != 0:
        B = ((A % 8) ^ 3) ^ (A >> ((A % 8) ^ 5))
        A = A >> 3
        output.append(B % 8)
    return output


def program_step(A):
    return (((A % 8) ^ 3) ^ (A >> ((A % 8) ^ 5))) % 8


def decode_input(A, output):
    if len(output) == 0:
        return [A]

    ans = []
    for suffix in range(8):
        if program_step((A << 3) + suffix) == output[-1]:
            ans.extend(decode_input((A << 3) + suffix, output[:-1]))
    return ans


def part1(text):
    left, right = text.split('\n\n')
    registers = Registers(*map(int, re.findall('\d+', left)))
    program = list(map(int, right.split()[1].split(',')))
    return run_program(program, registers)


def part2(text):
    _left, right = text.split('\n\n')
    program = list(map(int, right.split()[1].split(',')))
    return min(decode_input(0, program))
