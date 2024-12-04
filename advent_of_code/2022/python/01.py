def part1(text):
    calories = list(sum(map(int, group.split())) for group in text.split('\n\n'))
    return max(calories)


def part2(text):
    calories = list(sum(map(int, group.split())) for group in text.split('\n\n'))
    return sum(sorted(calories)[-3:])
