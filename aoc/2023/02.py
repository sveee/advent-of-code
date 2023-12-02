import numpy as np

from aoc.utils import get_input

text = get_input(day=2, year=2023)
minimum_cubes = []
for line in text.splitlines():
    game, cubes = line.split(':')
    _, game_id = game.split()
    cube_values = dict(red=[], green=[], blue=[])
    for cube_set in cubes.split(';'):
        for cube_value in cube_set.split(','):
            value, color = cube_value.split()
            cube_values[color].append(int(value))
    minimum_cubes.append([max(values) for values in cube_values.values()])
minimum_cubes = np.array(minimum_cubes)
print(sum(np.where(np.all(minimum_cubes <= [12, 13, 14], axis=1))[0] + 1))
print(np.prod(minimum_cubes, axis=1).sum())
