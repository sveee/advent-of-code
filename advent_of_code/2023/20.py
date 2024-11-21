import math
from collections import Counter, defaultdict, deque
from enum import Enum
from itertools import chain


class Module(Enum):
    FLIP_FLOP = 'flip_flop'
    CONJUNCTION = 'conjunction'
    BROADCASTER = 'broadcaster'
    UNTYPED = 'untyped'


class Pulse(Enum):
    HIGH = 'high'
    LOW = 'low'


def press_button(
    is_flip_flop_on, conjunction_memory, module_type, graph, terminal_module=None
):
    counter = Counter()
    queue = deque([('broadcaster', None, Pulse.LOW)])
    while len(queue) > 0:
        module, prev_module, pulse = queue.popleft()
        counter[pulse] += 1

        if pulse == Pulse.LOW and module == terminal_module:
            return True

        if module_type[module] == Module.FLIP_FLOP:
            if pulse == Pulse.LOW:
                next_pulse = Pulse.HIGH if not is_flip_flop_on[module] else Pulse.LOW
                is_flip_flop_on[module] ^= True
            elif pulse == Pulse.HIGH:
                next_pulse = None
        elif module_type[module] == Module.CONJUNCTION:
            conjunction_memory[module][prev_module] = pulse
            next_pulse = (
                Pulse.LOW
                if all(
                    prev_pulse == Pulse.HIGH
                    for prev_pulse in conjunction_memory[module].values()
                )
                else Pulse.HIGH
            )
        elif module_type[module] == Module.BROADCASTER:
            next_pulse = pulse
        elif module_type[module] == Module.UNTYPED:
            next_pulse = None

        if next_pulse is not None:
            for next_module in graph[module]:
                queue.append((next_module, module, next_pulse))

    if terminal_module:
        return False

    return counter


def read_input(text):
    graph = {}
    module_type = {}
    for line in text.splitlines():
        source, destinations = line.split(' -> ')
        if source == 'broadcaster':
            module_type[source] = Module.BROADCASTER
        else:
            prefix, source = source[0], source[1:]
            module_type[source] = (
                Module.FLIP_FLOP if prefix == '%' else Module.CONJUNCTION
            )
        destinations = destinations.split(', ')
        graph[source] = destinations
    for module in chain(*graph.values()):
        if module not in module_type:
            module_type[module] = Module.UNTYPED
    return graph, module_type


def create_memory(graph, module_type):
    is_flip_flop_on = {}
    conjunction_memory = defaultdict(dict)
    for module, next_modules in graph.items():
        if module_type[module] == Module.FLIP_FLOP:
            is_flip_flop_on[module] = False
        for next_module in next_modules:
            if module_type[next_module] == Module.CONJUNCTION:
                conjunction_memory[next_module][module] = Pulse.LOW
    return is_flip_flop_on, conjunction_memory


def part1(text, n_presses=1000):
    graph, module_type = read_input(text)
    is_flip_flop_on, conjunction_memory = create_memory(graph, module_type)
    counter = Counter()
    for _ in range(n_presses):
        counter += press_button(is_flip_flop_on, conjunction_memory, module_type, graph)
    return counter[Pulse.HIGH] * counter[Pulse.LOW]


def find_n_presses(graph, module_type, terminal_module):
    is_flip_flop_on, conjunction_memory = create_memory(graph, module_type)
    n_presses = 0
    while True:
        n_presses += 1
        if press_button(
            is_flip_flop_on, conjunction_memory, module_type, graph, terminal_module
        ):
            break
    return n_presses


def get_subgraph(node, graph):
    stack = [node]
    visited = set()
    while len(stack) > 0:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        if node not in graph:
            continue
        for next_node in graph[node]:
            stack.append(next_node)

    return {
        node: [next_node for next_node in graph[node] if next_node in visited]
        for node in graph
        if node in visited
    }


def part2(text):
    graph, module_type = read_input(text)
    n_terminal_presses = []
    for start_module in graph['broadcaster']:
        subgraph = get_subgraph(start_module, graph)
        subgraph['broadcaster'] = [start_module]
        n_terminal_presses.append(
            find_n_presses(subgraph, module_type, terminal_module='rx')
        )
    return math.lcm(*n_terminal_presses)
