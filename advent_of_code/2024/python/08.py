from collections import defaultdict
from itertools import combinations
from typing import NamedTuple


def within_bounds(x, y, n, m):
    return 0 <= x < n and 0 <= y < m


class Point(NamedTuple):
    x: int
    y: int


def get_antennas(grid):
    antennas = defaultdict(list)
    for x, line in enumerate(grid):
        for y, v in enumerate(line):
            if v != '.':
                antennas[v].append(Point(x, y))
    return antennas


def part1(text):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])
    antennas = get_antennas(grid)
    locations = set()
    for group in antennas.values():
        for a1, a2 in combinations(group, 2):
            an1 = Point(2 * a1.x - a2.x, 2 * a1.y - a2.y)
            an2 = Point(2 * a2.x - a1.x, 2 * a2.y - a1.y)
            if within_bounds(an1.x, an1.y, n, m):
                locations.add(an1)
            if within_bounds(an2.x, an2.y, n, m):
                locations.add(an2)
    return len(locations)


def part2(text):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])
    antennas = get_antennas(grid)
    locations = set()
    for group in antennas.values():
        for a1, a2 in combinations(group, 2):
            d = Point(a2[0] - a1[0], a2[1] - a1[1])
            an = a1
            while within_bounds(an.x, an.y, n, m):
                locations.add(an)
                an = Point(an.x - d.x, an.y - d.y)
            an = a2
            while within_bounds(an.x, an.y, n, m):
                locations.add(an)
                an = Point(an.x + d.x, an.y + d.y)
    return len(locations)
