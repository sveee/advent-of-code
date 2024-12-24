import re
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Gate:
    left: str
    right: str
    op: str
    output: str


def run_operations(values, gates):
    values = values.copy()
    gates_by_operand = defaultdict(list)
    for gate in gates:
        gates_by_operand[gate.left].append(gate)
        gates_by_operand[gate.right].append(gate)

    in_degree = defaultdict(int)
    for gate in gates:
        for next_gate in gates_by_operand[gate.output]:
            in_degree[next_gate] += 1

    zero_degrees = [gate for gate in gates if in_degree.get(gate, 0) == 0]

    while len(zero_degrees) > 0:
        gate = zero_degrees.pop()
        match gate.op:
            case 'AND':
                values[gate.output] = values[gate.left] & values[gate.right]
            case 'OR':
                values[gate.output] = values[gate.left] | values[gate.right]
            case 'XOR':
                values[gate.output] = values[gate.left] ^ values[gate.right]

        for next_gate in gates_by_operand[gate.output]:
            in_degree[next_gate] -= 1
            if in_degree[next_gate] == 0:
                zero_degrees.append(next_gate)
    return values


def parse_gates(text):
    gates = set()
    for line in text.splitlines():
        left, op, right, output = re.search(
            '([^\s]+) ([^\s]+) ([^\s]+) -> ([^\s]+)', line
        ).groups()
        gates.add(Gate(left, right, op, output))
    return gates


def part1(text):
    x_value_lines, gates_lines = text.split('\n\n')
    values = {}
    for line in x_value_lines.splitlines():
        x, value = re.search('(.+): (\d)', line).groups()
        values[x] = int(value)

    gates = parse_gates(gates_lines)
    z_gates = sorted(
        [
            (name, value)
            for name, value in run_operations(values, gates).items()
            if name.startswith('z')
        ],
        reverse=True,
    )
    return int(''.join(str(value) for _, value in z_gates), 2)


def get_first_n_gates(n, gates):
    gate_by_output = {}
    for gate in gates:
        gate_by_output[gate.output] = gate

    stack = [gate_by_output[f'z{index:02d}'] for index in range(n + 1)]
    subset_gates = set(stack)
    while len(stack) > 0:
        gate = stack.pop()
        if (
            gate.left in gate_by_output
            and gate_by_output[gate.left] not in subset_gates
        ):
            stack.append(gate_by_output[gate.left])
            subset_gates.add(gate_by_output[gate.left])
        if (
            gate.right in gate_by_output
            and gate_by_output[gate.right] not in subset_gates
        ):
            stack.append(gate_by_output[gate.right])
            subset_gates.add(gate_by_output[gate.right])
    return subset_gates - {gate_by_output[f'z{n:02d}']}


def is_valid_z(index, expected, values):
    z_name = f'z{index:02d}'
    return z_name in values and values[z_name] == expected


def passes_test1(n, gates):
    input_values = {}
    for index in range(n):
        input_values[f'x{index:02d}'] = 0
        input_values[f'y{index:02d}'] = 1
    input_values[f'x{n:02d}'] = input_values[f'y{n:02d}'] = 0
    output_values = run_operations(input_values, gates)
    for index in range(n):
        if not is_valid_z(index, 1, output_values):
            return False
    return True


def passes_test2(n, gates):
    input_values = {}
    for index in range(n):
        input_values[f'x{index:02d}'] = 0
        input_values[f'y{index:02d}'] = 1
    input_values['x00'] = 1
    input_values[f'x{n:02d}'] = input_values[f'y{n:02d}'] = 0
    output_values = run_operations(input_values, gates)
    for index in range(n):
        if not is_valid_z(index, 0, output_values):
            return False
    return True


def passes_test3(n, gates):
    input_values = {}
    for index in range(n):
        input_values[f'x{index:02d}'] = 1
        input_values[f'y{index:02d}'] = 1
    input_values[f'x{n:02d}'] = input_values[f'y{n:02d}'] = 0
    output_values = run_operations(input_values, gates)
    if not is_valid_z(0, 0, output_values):
        return
    for index in range(1, n):
        if not is_valid_z(index, 1, output_values):
            return False
    return True


def are_valid_gates(n, gates):
    return passes_test1(n, gates) and passes_test2(n, gates) and passes_test3(n, gates)


@dataclass
class GatesSwap:
    prev_gates: set[Gate]
    new_gates: set[Gate]
    swapped_outputs: tuple[str, str]


def swap_gates(gate1, gate2):
    return GatesSwap(
        {gate1, gate2},
        {
            Gate(gate1.left, gate1.right, gate1.op, gate2.output),
            Gate(gate2.left, gate2.right, gate2.op, gate1.output),
        },
        [gate1.output, gate2.output],
    )


def get_possible_fixes(gates):
    gates = sorted(gates)
    possible_fixes = []
    for index, gate1 in enumerate(gates):
        for gate2 in gates[index + 1 :]:
            possible_fixes.append(swap_gates(gate1, gate2))
    return possible_fixes


def part2(text):
    _, gates_lines = text.split('\n\n')
    gates = parse_gates(gates_lines)

    swapped_outputs = []
    for n in range(1, 45):
        first_n_gates = get_first_n_gates(n, gates)
        if not are_valid_gates(n, first_n_gates):
            gates_to_fix = first_n_gates - get_first_n_gates(n - 2, gates)
            for possible_fix in get_possible_fixes(gates_to_fix):
                new_gates = (gates - possible_fix.prev_gates) | possible_fix.new_gates
                if are_valid_gates(n, get_first_n_gates(n, new_gates)):
                    gates = new_gates
                    swapped_outputs.extend(possible_fix.swapped_outputs)
                    break
    return ','.join(sorted(swapped_outputs))
