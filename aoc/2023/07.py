from collections import Counter
from enum import Enum

from aoc.problem import Problem

card_map = {
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}


class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


counts_map = {
    (5,): HandType.FIVE_OF_A_KIND.value,
    (1, 4): HandType.FOUR_OF_A_KIND.value,
    (2, 3): HandType.FULL_HOUSE.value,
    (1, 1, 3): HandType.THREE_OF_A_KIND.value,
    (1, 2, 2): HandType.TWO_PAIR.value,
    (1, 1, 1, 2): HandType.ONE_PAIR.value,
    (1, 1, 1, 1, 1): HandType.HIGH_CARD.value,
}


def hand_value(hand):
    values = [card_map.get(card) if card in card_map else int(card) for card in hand]
    counts = Counter(values)
    return (
        counts_map[tuple(sorted(counts.values()))],
        tuple(values),
    )


class Promblem2023_07(Problem):
    def solve(self, text):
        hands = [line.split() for line in text.splitlines()]
        hands = sorted(hands, key=lambda x: hand_value(x[0]))
        self.part1 = sum(
            (index + 1) * int(bit) for index, (_hand, bit) in enumerate(hands)
        )
        self.part2 = None


Promblem2023_07().check_test()
Promblem2023_07().submit()

# print(hand_value('23456'))
