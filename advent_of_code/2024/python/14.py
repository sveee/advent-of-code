import re
from collections import defaultdict
from functools import reduce
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def get_quadrant(p, v, s, k):
    x = (p.x + k * (v.x + s.x)) % s.x
    y = (p.y + k * (v.y + s.y)) % s.y
    mx, my = s.x // 2, s.y // 2
    if x > mx and y < my:
        return 1
    if x < mx and y < my:
        return 2
    if x < mx and y > my:
        return 3
    if x > mx and y > my:
        return 4


def part1(text, w=101, h=103, k=100):
    s = Point(w, h)
    n_per_quadrant = defaultdict(int)
    for line in text.splitlines():
        px, py, vx, vy = re.search('p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line).groups()
        if quadrant_id := get_quadrant(
            Point(int(px), int(py)),
            Point(int(vx), int(vy)),
            s,
            k,
        ):
            n_per_quadrant[quadrant_id] += 1
    return reduce(
        lambda a, b: a * b,
        n_per_quadrant.values(),
    )


def part2(text):
    pass
