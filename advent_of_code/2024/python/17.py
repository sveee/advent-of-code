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


def part1(text):
    left, right = text.split('\n\n')
    registers = Registers(*map(int, re.findall('\d+', left)))
    program = list(map(int, right.split()[1].split(',')))
    return run_program(program, registers)


def part2(text):
    pass
