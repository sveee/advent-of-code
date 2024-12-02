
def is_safe(level):
    return (
        all(1<= abs(a-b) <= 3 for a, b in zip(level, level[1:]))
        and (
            all(a > b for a, b in zip(level, level[1:]))
            or
            all(a < b for a, b in zip(level, level[1:]))
        )
    )


def part1(text):
    total = 0
    for line in text.splitlines():
        level = list(map(int, line.split()))
        total += is_safe(level)
    return total

def part2(text):
    total = 0
    for line in text.splitlines():
        level = list(map(int, line.split()))
        safe = False
        if not is_safe(level):
            for i in range(len(level)):
                if is_safe(level[:i] + level[i + 1: ]):
                    safe = True
                    break
        else:
            safe = True
        # print(level, safe)
        total += safe
    return total
