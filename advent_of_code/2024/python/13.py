import re
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


def min_tokens(da, db, p):
    # da.x, db.x  *   na   =   p.x
    # da.y, db.y      nb       p.y

    D = da.x * db.y - da.y * db.x
    A = p.x  * db.y - p.y  * db.x
    B = da.x *  p.y - da.y *  p.x

    if D < 0:
        A *= -1
        B *= -1
        D *= -1

    if A % D == 0 and B % D == 0:
        return 3 * A // D + B // D
    
    return 0

def get_machines(text):
    machines = []
    for machine in text.split('\n\n'):
        button_a, button_b, prize = machine.splitlines()
        da = Point(*map(int, re.findall('\d+', button_a)))
        db = Point(*map(int, re.findall('\d+', button_b)))
        p = Point(*map(int, re.findall('\d+', prize)))
        machines.append((da, db, p))
    return machines

def part1(text):
    return sum(
        min_tokens(da, db, p)
        for da, db, p in get_machines(text)
    )

N = 10000000000000

def part2(text):
    return sum(
        min_tokens(da, db, Point(p.x+N,p.y+N))
        for da, db, p in get_machines(text)
    )
