import numpy as np
from itertools import product
from scipy.optimize import linprog
from functools import reduce


def solve_diagram(lights, buttons):
    min_presses = 10**10
    for presses in product([False, True], repeat=len(buttons)):
        current_lights = [0 for _ in lights]
        for press, button in zip(presses, buttons):
            if not press:
                continue
            for light in button:
                current_lights[light] ^= 1
        if current_lights == lights:
            min_presses = min(min_presses, sum(presses))
    return min_presses


def part1(text):
    total = 0
    for line in text.splitlines():
        parts = line.split()
        light_diagram = [int(l == '#') for l in parts[0][1:-1]]
        buttons = [set(map(int, part[1:-1].split(','))) for part in parts[1:-1]]
        total += solve_diagram(light_diagram, buttons)
    return total


def part2(text):
    total = 0
    for line in text.splitlines():
        parts = line.split()
        b_eq = np.array(list(map(int, parts[-1][1:-1].split(','))))
        button_sets = [set(map(int, part[1:-1].split(','))) for part in parts[1:-1]]
        A_eq = np.array(
            [
                [int(n in button_set) for n in range(len(b_eq))]
                for button_set in button_sets
            ]
        ).T
        c = np.ones(A_eq.shape[1], dtype=int)
        res = linprog(
            c, A_eq=A_eq, b_eq=b_eq, bounds=(0, b_eq.max() + 1), integrality=1
        )
        int_x = np.rint(res.x).astype(int)
        print(reduce(lambda x, y: x * y, b_eq))
        total += int_x.sum()
    return total
