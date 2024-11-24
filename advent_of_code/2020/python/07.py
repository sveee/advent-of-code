import re
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class BagCount:
    name: str
    count: int


SHINY_GOLD_BAG = 'shiny gold bag'
NO_OTHER_BAG = 'no other bag'


def normalize(s):
    return s.rstrip('s')


def get_bag_counts(text):
    bag_counts = defaultdict(list)
    for line in text.splitlines():
        left, rights = line.rstrip('.').split(' contain ')
        for right in rights.split(', '):
            right = normalize(right)
            count, name = (
                re.search(r'(\d+) (.*)', right).groups()
                if right != NO_OTHER_BAG
                else (0, right)
            )
            bag_counts[normalize(left)].append(BagCount(name, int(count)))
    return bag_counts


def contains_shiny_gold(bag, bag_counts):
    if bag == NO_OTHER_BAG:
        return False
    if bag == SHINY_GOLD_BAG:
        return True
    for bag_count in bag_counts[bag]:
        if contains_shiny_gold(bag_count.name, bag_counts):
            return True
    return False


def get_count(bag, bag_counts):
    if bag == NO_OTHER_BAG:
        return 0
    return (
        sum(
            other_bag.count * get_count(other_bag.name, bag_counts)
            for other_bag in bag_counts[bag]
        )
        + 1
    )


def part1(text):
    bag_counts = get_bag_counts(text)
    return sum(
        contains_shiny_gold(bag, bag_counts)
        for bag in list(bag_counts)
        if bag != SHINY_GOLD_BAG
    )


def part2(text):
    bag_counts = get_bag_counts(text)
    return get_count(SHINY_GOLD_BAG, bag_counts) - 1
