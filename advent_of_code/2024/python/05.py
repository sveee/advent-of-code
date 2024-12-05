
from collections import defaultdict

def are_ordered(pages, rules):
    return all(
        right in rules[left]
        for left, right in zip(pages, pages[1:])
    )


def part1(text):
    ordering_rules, pages_in_update = text.split('\n\n')

    rules = defaultdict(list)
    for line in ordering_rules.splitlines():
        left, right = line.split('|')
        rules[left].append(right)

    total = 0
    for line in pages_in_update.splitlines():
        pages = line.split(',')
        if are_ordered(pages, rules):
            total += int(pages[len(pages) // 2])
    return total


def part2(text):
    pass
