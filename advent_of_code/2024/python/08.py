
from collections import defaultdict
from itertools import combinations


def within_bounds(x, y, n, m):
    return 0 <= x < n and 0 <= y < m

def part1(text):
    grid = text.splitlines()
    antennas = defaultdict(list)
    for x, line in enumerate(grid):
        for y, v in enumerate(line):
            if v != '.':
                antennas[v].append((x, y))

    locations = set()
    for group in antennas.values():
        for a1, a2 in combinations(group, 2):
            an1 = 2*a1[0] - a2[0], 2*a1[1] - a2[1]
            an2 = 2*a2[0] - a1[0], 2*a2[1] - a1[1]
            if within_bounds(*an1, len(grid), len(grid[0])):
                locations.add(an1)
            if within_bounds(*an2, len(grid), len(grid[0])):
                locations.add(an2)
    return len(locations)



def part2(text):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])
    antennas = defaultdict(list)
    for x, line in enumerate(grid):
        for y, v in enumerate(line):
            if v != '.':
                antennas[v].append((x, y))

    locations = set()
    for group in antennas.values():
        for a1, a2 in combinations(group, 2):
            d = a2[0] - a1[0], a2[1] - a1[1]
            an = a1
            while within_bounds(*an, n, m ):
                locations.add(an)
                an = an[0] - d[0], an[1] - d[1]
            an = a2
            while within_bounds(*an, n, m ):
                locations.add(an)
                an = an[0] + d[0], an[1] + d[1]
    return len(locations)

