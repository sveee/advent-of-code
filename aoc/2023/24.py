from dataclasses import dataclass


@dataclass
class Vector:
    x: int
    y: int
    z: int

    def from_str(s: str) -> 'Vector':
        return Vector(*map(int, s.split(', ')))


@dataclass
class Hailstone:
    posiiton: Vector
    velocity: Vector


EPS = 1e-7


def do_intersect_inside(hailstone1, hailstone2, min_value, max_value):
    # we solve p1 + t1 * v1 = p2 + t2 * v2
    # solution is t1 = D[p2 - p1 | -v2 ] / D[v1 | -v2]
    D = (
        hailstone1.velocity.x * -hailstone2.velocity.y
        - hailstone1.velocity.y * -hailstone2.velocity.x
    )
    if D == 0:
        return False

    N1 = (hailstone2.posiiton.x - hailstone1.posiiton.x) * -hailstone2.velocity.y - (
        hailstone2.posiiton.y - hailstone1.posiiton.y
    ) * -hailstone2.velocity.x
    N2 = (
        hailstone1.velocity.x * (hailstone2.posiiton.y - hailstone1.posiiton.y)
        - hailstone1.velocity.y * (hailstone2.posiiton.x - hailstone1.posiiton.x)
    )

    t1 = N1 / D
    t2 = N2 / D

    if t1 < 0 or t2 < 0:
        return False

    x = hailstone1.posiiton.x + hailstone1.velocity.x * t1
    y = hailstone1.posiiton.y + hailstone1.velocity.y * t1


    return (
        min_value - EPS <= x <= max_value + EPS
        and min_value - EPS <= y <= max_value + EPS
    )


def part1(text, min_value=200000000000000, max_value=400000000000000):
    hailstones = []
    for line in text.splitlines():
        position, velocity = line.split(' @ ')
        hailstones.append(
            Hailstone(Vector.from_str(position), Vector.from_str(velocity))
        )

    n_intersections = 0
    for index, hailstone1 in enumerate(hailstones):
        for hailstone2 in hailstones[index + 1 :]:
            if do_intersect_inside(hailstone1, hailstone2, min_value, max_value):
                n_intersections += 1
    return n_intersections


def part2(text):
    pass
