import re
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Connection:
    left: str
    right: str
    output: str
    op: str


def run_wires(connections, gates):
    connections_by_operand = defaultdict(list)
    for connection in connections:
        connections_by_operand[connection.left].append(connection)
        connections_by_operand[connection.right].append(connection)

    in_degree = defaultdict(int)
    for connection in connections:
        for next_connection in connections_by_operand[connection.output]:
            in_degree[next_connection] += 1

    zero_degrees = [
        connection for connection in connections if in_degree.get(connection, 0) == 0
    ]

    while len(zero_degrees) > 0:
        connection = zero_degrees.pop()
        match connection.op:
            case 'AND':
                gates[connection.output] = (
                    gates[connection.left] & gates[connection.right]
                )
            case 'OR':
                gates[connection.output] = (
                    gates[connection.left] | gates[connection.right]
                )
            case 'XOR':
                gates[connection.output] = (
                    gates[connection.left] ^ gates[connection.right]
                )

        for next_connection in connections_by_operand[connection.output]:
            in_degree[next_connection] -= 1
            if in_degree[next_connection] == 0:
                zero_degrees.append(next_connection)


def part1(text):
    x_value_lines, connection_lines = text.split('\n\n')
    gates = {}
    for line in x_value_lines.splitlines():
        x, value = re.search('(.+): (\d)', line).groups()
        gates[x] = int(value)

    connections = []
    for line in connection_lines.splitlines():
        left, op, right, output = re.search(
            '([^\s]+) ([^\s]+) ([^\s]+) -> ([^\s]+)', line
        ).groups()
        connections.append(Connection(left, right, output, op))

    run_wires(connections, gates)

    z_gates = sorted(
        [(name, value) for name, value in gates.items() if name.startswith('z')],
        reverse=True,
    )
    return int(''.join(str(value) for _, value in z_gates), 2)


def part2(text):
    pass
