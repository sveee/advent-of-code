import re


def read_input(text):
    instructions, network = text.split('\n\n')
    graph = {}
    for line in network.splitlines():
        source, *destinations = re.search('(\w+) = \((\w+), (\w+)\)', line).groups()
        graph[source] = destinations
    return graph, instructions


def gcd2(x, y):
    while y:
        x, y = y, x % y
    return x


def lcm2(x, y):
    return (x * y) // gcd2(x, y)


def lcm(numbers):
    result = numbers[0]
    for number in numbers[1:]:
        result = lcm2(result, number)
    return result


def find_cycle_size(node, graph, instructions):
    index = 0
    while True:
        if node.endswith('Z'):
            return index
        node = graph[node][0 if instructions[index % len(instructions)] == 'L' else 1]
        index += 1


def part1(text):
    graph, instructions = read_input(text)
    return find_cycle_size('AAA', graph, instructions)


def part2(text):
    graph, instructions = read_input(text)
    return lcm(
        [
            find_cycle_size(node, graph, instructions)
            for node in [node for node in graph if node.endswith('A')]
        ]
    )
