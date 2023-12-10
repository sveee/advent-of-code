import math
from functools import reduce

from aoc.problem import Problem


def n_ways_to_win(time, distance):
    D = math.sqrt(time * time - 4 * distance)
    x1, x2 = (time - D) / 2, (time + D) / 2
    answer = math.floor(x2) - math.ceil(x1) + 1
    if x1 == math.ceil(x1):
        # If x1 is an integer, then x2 is also an integer. Follows from Vieta's formulas.
        answer -= 2
    return answer


class Problem2023_06(Problem):
    def part1(self, text):
        times, distances = map(
            lambda x: list(map(int, x.split(':')[1].split())), text.splitlines()
        )
        return reduce(
            lambda x, y: x * y,
            [n_ways_to_win(time, distance) for time, distance in zip(times, distances)],
        )

    def part2(self, text):
        times, distances = map(
            lambda x: list(map(int, x.split(':')[1].split())), text.splitlines()
        )
        return n_ways_to_win(
            int(''.join(map(str, times))),
            int(''.join(map(str, distances))),
        )
