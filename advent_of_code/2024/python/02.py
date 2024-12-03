def is_safe(level):
    return all(1 <= abs(a - b) <= 3 for a, b in zip(level, level[1:])) and (
        all(a > b for a, b in zip(level, level[1:]))
        or all(a < b for a, b in zip(level, level[1:]))
    )


def is_almost_safe(level):
    return any(is_safe(level[:i] + level[i + 1 :]) for i in range(len(level)))


def part1(text):
    return sum(is_safe(list(map(int, line.split()))) for line in text.splitlines())


def part2(text):
    return sum(
        is_safe(level) or is_almost_safe(level)
        for line in text.splitlines()
        if (level := list(map(int, line.split())))
    )
