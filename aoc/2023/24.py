from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from typing import NamedTuple

import numpy as np


class Vector(NamedTuple):
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
    # We solve p1 + t1 * v1 = p2 + t2 * v2.
    # The solution is t1 = D[p2 - p1|-v2 ] / D[v1|-v2]
    D = (
        hailstone1.velocity.x * -hailstone2.velocity.y
        - hailstone1.velocity.y * -hailstone2.velocity.x
    )
    if D == 0:
        return False

    N1 = (hailstone2.posiiton.x - hailstone1.posiiton.x) * -hailstone2.velocity.y - (
        hailstone2.posiiton.y - hailstone1.posiiton.y
    ) * -hailstone2.velocity.x
    N2 = hailstone1.velocity.x * (
        hailstone2.posiiton.y - hailstone1.posiiton.y
    ) - hailstone1.velocity.y * (hailstone2.posiiton.x - hailstone1.posiiton.x)
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


def get_hailstones(text):
    hailstones = []
    for line in text.splitlines():
        position, velocity = line.split(' @ ')
        hailstones.append(
            Hailstone(Vector.from_str(position), Vector.from_str(velocity))
        )
    return hailstones


def part1(text, min_value=200000000000000, max_value=400000000000000):
    hailstones = get_hailstones(text)
    n_intersections = 0
    for index, hailstone1 in enumerate(hailstones):
        for hailstone2 in hailstones[index + 1 :]:
            if do_intersect_inside(hailstone1, hailstone2, min_value, max_value):
                n_intersections += 1
    return n_intersections


def get_determinant(A):
    return (
        A[0][0] * A[1][1] * A[2][2]
        + A[0][1] * A[1][2] * A[2][0]
        + A[0][2] * A[2][1] * A[1][0]
        - A[0][2] * A[1][1] * A[2][0]
        - A[0][1] * A[1][0] * A[2][2]
        - A[0][0] * A[2][1] * A[1][2]
    )


def solve(A, b):
    D = get_determinant(A)
    if D == 0:
        return
    AB = [deepcopy(A) for _ in range(3)]
    for j in range(3):
        for i in range(3):
            AB[j][i][j] = b[i]
    B = [get_determinant(AB[i]) for i in range(3)]
    for i in range(3):
        if B[i] % D != 0:
            return
    return B[0] // D, B[1] // D, B[2] // D


def multiply(A, b):
    return [sum(a_i * b_i for a_i, b_i in zip(a, b)) for a in A]


def get_equations(velocity, hailstones, only_3=True):
    # If we know the rv, the rp equations are:
    # rpx*(hvy - rvy) + rpy*(rvx - hvx) = hpx*hvy + rvx*hpy - hpx*rvy - hvx*hpy
    # rpy*(hvz - rvz) + rpz*(rvy - hvy) = hpy*hvz + rvy*hpz - hpy*rvz - hvy*hpz
    # If we transform the equation into 3x3 matrix with rows a1, a2, a3 we get:
    # a1 = [hvy - rvy, rvx - hvx, 0], b1 = hpx*hvy + rvx*hpy - hpx*rvy - hvx*hpy
    # a2 = [0, hvz - rvz, rvy - hvy], b2 = hpy*hvz + rvy*hpz - hpy*rvz - hvy*hpz
    rvx, rvy, rvz = velocity
    A, b = [], []
    for hailstone in hailstones:
        hpx, hpy, hpz = hailstone.posiiton
        hvx, hvy, hvz = hailstone.velocity
        A.append([hvy - rvy, rvx - hvx, 0])
        b.append(hpx * hvy + rvx * hpy - hpx * rvy - hvx * hpy)
        A.append([0, hvz - rvz, rvy - hvy])
        b.append(hpy * hvz + rvy * hpz - hpy * rvz - hvy * hpz)
    if only_3:
        A3, b3, index = [], [], 0
        for index in range(len(A)):
            if len(A3) == 3:
                break
            prev_rank = np.linalg.matrix_rank(np.array(A3)) if len(A3) > 0 else 0
            if (
                len(A3) == 0
                or np.linalg.matrix_rank(np.array(A3 + [A[index]])) != prev_rank
            ):
                A3.append(A[index])
                b3.append(b[index])
        assert len(A3) == 3 and len(b3) == 3
        A, b = A3, b3
    return A, b


# # For part 2 we can use scipy.fsolve but it return inaccurate solution
# from scipy.optimize import fsolve

#     def equations(vars):
#         rpx, rpy, rpz, rvx, rvy, rvz = vars
#         values = []
#         start = 0
#         for hailstone in hailstones[start:start + 3]:
#             hpx, hpy, hpz = hailstone.posiiton.x, hailstone.posiiton.y, hailstone.posiiton.z
#             hvx, hvy, hvz = hailstone.velocity.x, hailstone.velocity.y, hailstone.velocity.z
#             values.append(rpx*hvy - hpx*hvy - rpx*rvy + hpx*rvy - hvx*rpy + rvx*rpy + hvx*hpy - rvx*hpy)
#             values.append(rpy*hvz - hpy*hvz - rpy*rvz + hpy*rvz - hvy*rpz + rvy*rpz + hvy*hpz - rvy*hpz)
#         return values

#     x_init = max(hailstone.posiiton.x for hailstone in hailstones)
#     y_init = max(hailstone.posiiton.y for hailstone in hailstones)
#     z_init = max(hailstone.posiiton.z for hailstone in hailstones)
#     solution = fsolve(equations, [x_init / 2, y_init/2, z_init/2 , 0, 0, 0])
#     print(list(map(lambda x: round(x), solution)))


def part2(text):
    hailstones = get_hailstones(text)
    for rv in product(range(240, 300), range(60, 100), range(100, 200)):
        A, b = get_equations(rv, hailstones)
        rp = solve(A, b)

        if rp:
            A, b = get_equations(rv, hailstones, only_3=False)

            if all(b1 == b2 for b1, b2 in zip(multiply(A, rp), b)):
                print(rv, rp)
                return sum(rp)
