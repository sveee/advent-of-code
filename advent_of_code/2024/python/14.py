import re
from collections import defaultdict
from functools import reduce
from typing import NamedTuple, Self

from tqdm import tqdm

DIRECTIONS = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0]


class Point(NamedTuple):
    x: int
    y: int


class Robot(NamedTuple):
    position: Point
    velocity: Point

    def move(self, size: Point) -> Self:
        return Robot(
            Point(
                (self.position.x + self.velocity.x + size.x) % size.x,
                (self.position.y + self.velocity.y + size.y) % size.y,
            ),
            self.velocity,
        )


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


def count_components(positions, size):
    visited = set()

    def _flood_fill(p):
        stack = [p]
        visited.add(p)
        while stack:
            p = stack.pop()
            for dx, dy in DIRECTIONS:
                np = Point(p.x + dx, p.y + dy)
                if (
                    0 <= np.x < size.x
                    and 0 <= np.y < size.y
                    and np not in visited
                    and np in positions
                ):
                    visited.add(np)
                    stack.append(np)

    n_components = 0
    for position in positions:
        if position not in visited:
            _flood_fill(position)
            n_components += 1
    return n_components


def part2(text, w=101, h=103):
    robots = []
    size = Point(w, h)
    for line in text.splitlines():
        px, py, vx, vy = re.search('p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line).groups()
        robots.append(
            Robot(
                Point(int(px), int(py)),
                Point(int(vx), int(vy)),
            )
        )

    min_n_components, tree_seconds = len(robots), 0
    for seconds in tqdm(list(range(w * h))):
        n_components = count_components(
            [robot.position for robot in robots],
            size,
        )
        if n_components < min_n_components:
            min_n_components = n_components
            tree_seconds = seconds
        robots = [robot.move(size) for robot in robots]
    return tree_seconds
