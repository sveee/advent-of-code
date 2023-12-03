from aoc.utils import get_full_input, get_test_answers, get_test_input
from typing import Tuple, Any
import re
from abc import abstractmethod


def _assert_equal(value: Any, expected: Any):
    return (
        '\033[92m' + '\033[1m' + 'PASS' + '\033[0m'
        if expected == value
        else '\033[91m' + '\033[1m' + 'FAIL' + '\033[0m' + f': {expected} != {value}'
    )


class Problem:
    def __init__(self) -> None:
        year, day = re.findall('\d+', self.__class__.__name__)
        self.year = int(year)
        self.day = int(day)
        self.part1 = None
        self.part2 = None

    @abstractmethod
    def solve_input(self, text: str) -> None:
        pass

    def solve(self) -> Tuple[Any, Any]:
        self.solve_input(get_full_input(self.day, self.year))
        print(self.part1)
        print(self.part2)

    def test(self, test1_index: int = 0, test2_index: int = 0):
        values = []
        self.solve_input(get_test_input(self.day, self.year, test1_index))
        values.append(self.part1)
        self.solve_input(get_test_input(self.day, self.year, test2_index))
        values.append(self.part2)
        test_answers = get_test_answers(self.day, self.year)

        for answer, value in zip(test_answers, values):
            if value is not None:
                print(_assert_equal(str(value), answer))