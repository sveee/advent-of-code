import re


def min_tokens(da, db, p):

    return min(
        [
            3 * na + nb
            for na in range(101)
            for nb in range(101)
            if na * da[0] + nb * db[0] == p[0] and na * da[1] + nb * db[1] == p[1]
        ],
        default=0,
    )


def part1(text):
    total = 0
    for machine in text.split('\n\n'):
        button_a, button_b, prize = machine.splitlines()
        da = tuple(map(int, re.findall('\d+', button_a)))
        db = tuple(map(int, re.findall('\d+', button_b)))
        p = tuple(map(int, re.findall('\d+', prize)))
        total += min_tokens(da, db, p)
    return total


def part2(text):
    pass
