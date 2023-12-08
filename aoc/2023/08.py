import re
from itertools import cycle

from aoc.problem import Problem


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def lcm2(x, y):
    return (x * y) // gcd(x, y)


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
            start, *destination = re.search('(\w+) = \((\w+), (\w+)\)', line).groups()
            graph[start] = destination

        node = 'AAA'
        n_steps = 0
        for instuction in cycle(instructions):
            if node == 'ZZZ':
                break
            node = graph[node][0 if instuction == 'L' else 1]
            n_steps += 1
        self.part1 = n_steps
        nodes = [node for node in graph if node.endswith('A')]
        self.part2 = lcm([find_cycle_size(node, graph, instructions) for node in nodes])


Promblem2023_08().print_solution()
