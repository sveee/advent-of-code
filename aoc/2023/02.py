import numpy as np

from aoc.problem import Problem


class Promblem2023_02(Problem):
    def solve_input(self, text):
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
        self.part1 = sum(np.where((required_cubes <= [12, 13, 14]).all(axis=1))[0] + 1)
        self.part2 = np.prod(required_cubes, axis=1).sum()


Promblem2023_02().solve()
