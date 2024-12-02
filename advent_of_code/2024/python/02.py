
def part1(text):
    total = 0
    for line in text.splitlines():
        level = list(map(int, line.split()))
        safe = (
            all(1<= abs(a-b) <= 3 for a, b in zip(level, level[1:]))
            and (
                all(a > b for a, b in zip(level, level[1:]))
                or
                all(a < b for a, b in zip(level, level[1:]))
            )
        )
        if safe:
            total += 1
    return total

def part2(text):
    pass
