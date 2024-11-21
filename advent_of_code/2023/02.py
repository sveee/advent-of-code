import numpy as np


def get_required_cubes(text):
    required_cubes = []
    for line in text.splitlines():
        _game, cubes = line.split(':')
        cube_values = dict(red=[], green=[], blue=[])
        for cube_set in cubes.split(';'):
            for cube_value in cube_set.split(','):
                value, color = cube_value.split()
                cube_values[color].append(int(value))
        required_cubes.append([max(values) for values in cube_values.values()])
    return np.array(required_cubes)


def part1(text):
    required_cubes = get_required_cubes(text)
    return sum(np.where((required_cubes <= [12, 13, 14]).all(axis=1))[0] + 1)


def part2(text):
    required_cubes = get_required_cubes(text)
    return np.prod(required_cubes, axis=1).sum()
