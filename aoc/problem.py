import re
from abc import abstractmethod
from typing import Any

from bs4 import BeautifulSoup

from aoc.api import get_full_input, get_problem_soup, post_request


def _equal_status(value: Any, expected: Any) -> str:
    return (
        '\033[92m' + '\033[1m' + 'PASS' + '\033[0m'
        if expected == value
        else '\033[91m' + '\033[1m' + 'FAIL' + '\033[0m' + f': {expected} != {value}'
    )


class Problem:
    def __init__(self) -> None:
        year, day = re.findall('\d+', self.__class__.__name__)
        self.year, self.day = int(year), int(day)

    @abstractmethod
    def part1(self, text: str) -> Any:
        pass

    @abstractmethod
    def part2(self, text: str) -> Any:
        pass

    def print_solution(self) -> None:
        full_input = get_full_input(self.year, self.day)
        print(f'Part1: {self.part1(full_input)}')
        print(f'Part2: {self.part2(full_input)}')

    def submit(self) -> None:
        soup = get_problem_soup(self.year, self.day)
        n_parts_solved = len(re.findall('Your puzzle answer was', soup.text))
        if n_parts_solved >= 2:
            print('Problem already solved!')
            return
        full_input = get_full_input(self.year, self.day)
        answer = (
            str(self.part1(full_input))
            if n_parts_solved == 0
            else str(self.part2(full_input))
        )
        if answer is None:
            return
        soup = BeautifulSoup(
            post_request(
                f'https://adventofcode.com/{self.year}/day/{self.day}/answer',
                dict(
                    level=n_parts_solved + 1,
                    answer=answer,
                ),
            ),
            features='html.parser',
        )
        print(re.sub('\s+', ' ', soup.find('article').text))
