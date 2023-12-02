import numpy as np

from aoc.utils import get_input

text = get_input(day=2, year=2023)
required_cubes = []
for line in text.splitlines():
    _game, cubes = line.split(':')
    cube_values = dict(red=[], green=[], blue=[])
    for cube_set in cubes.split(';'):
        for cube_value in cube_set.split(','):
            value, color = cube_value.split()
            cube_values[color].append(int(value))
    required_cubes.append([max(values) for values in cube_values.values()])
required_cubes = np.array(required_cubes)
print(sum(np.where((required_cubes <= [12, 13, 14]).all(axis=1))[0] + 1))
print(np.prod(required_cubes, axis=1).sum())
