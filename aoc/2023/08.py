import re
from itertools import cycle

from aoc.problem import Problem


def gcd2(x, y):
    while y:
        x, y = y, x % y
    return x


def lcm2(x, y):
    return (x * y) // gcd2(x, y)


def lcm(numbers):
    result = numbers[0]
    for i in range(1, len(numbers)):
        result = lcm2(result, numbers[i])
    return result


def find_cycle_size(node, graph, instructions):
    current_index, total_index = 0, 0
    while True:
        if node.endswith('Z'):
            return total_index
        node = graph[node][0 if instructions[current_index] == 'L' else 1]
        current_index += 1
        total_index += 1
        if current_index >= len(instructions):
            current_index = 0


class Promblem2023_08(Problem):
    def solve(self, text):
        instructions, network = text.split('\n\n')
        graph = {}
        for line in network.splitlines():
            start, *destinations = re.search('(\w+) = \((\w+), (\w+)\)', line).groups()
            graph[start] = destinations
        self.part1 = find_cycle_size('AAA', graph, instructions)
        self.part2 = lcm(
            [
                find_cycle_size(node, graph, instructions)
                for node in [node for node in graph if node.endswith('A')]
            ]
        )


Promblem2023_08().print_solution()
