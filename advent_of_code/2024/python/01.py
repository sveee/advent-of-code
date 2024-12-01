
def part1(text):
    left, right = zip(*[
        map(int, line.split())
        for line in text.splitlines()
    ])
    return sum(
        abs(a - b)
        for a, b in zip(sorted(left), sorted(right))
    )


def part2(text):
    pass
