import os
import re
from abc import abstractmethod
from typing import Any, List, Dict

import requests
from bs4 import BeautifulSoup

AOC_SESSION = os.environ['AOC_SESSION']


def get_request(url: str) -> str:
    return requests.get(
        url,
        cookies=dict(session=AOC_SESSION),
    ).text


def post_request(url: str, data: Dict[str, Any]) -> str:
    return requests.post(
        url,
        data=data,
        cookies=dict(session=AOC_SESSION),
    ).text


def _get_problem_soup(year: int, day: int) -> str:
    return BeautifulSoup(
        get_request(f'https://adventofcode.com/{year}/day/{day}'),
        features='html.parser',
    )


def _get_full_input(year: int, day: int) -> str:
    input_text = get_request(f'https://adventofcode.com/{year}/day/{day}/input')
    if input_text.endswith('\n'):
        input_text = input_text[:-1]
    return input_text


def _get_test_input(year: int, day: int, test_index: int = 0) -> str:
    soup = _get_problem_soup(year, day)
    input_text = soup.find_all('pre')[test_index].text
    if input_text.endswith('\n'):
        input_text = input_text[:-1]
    return input_text


def _get_test_answers(year: int, day: int) -> List[str]:
    soup = _get_problem_soup(year, day)
    parts = soup.find_all('article')
    return [
        [em.text for code in part.find_all('code') if (em := code.find('em'))][-1]
        for part in parts
    ]


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
        full_input = _get_full_input(self.year, self.day)
        print(f'Part1: {self.part1(full_input)}')
        print(f'Part2: {self.part2(full_input)}')

    # def check_test(self, test_index1: int = 0, test_index2: int = 0):
    #     # TODO: refactor
    #     values = []
    #     self.solve(_get_test_input(self.year, self.day, test_index1))
    #     values.append(self.part1)
    #     if self.part2 is not None:
    #         self.solve(_get_test_input(self.year, self.day, test_index2))
    #         values.append(self.part2)
    #     test_answers = _get_test_answers(self.year, self.day)
    #     for answer, value in zip(test_answers, values):
    #         if value is not None:
    #             print(_equal_status(str(value), answer))

    def submit(self) -> None:
        soup = _get_problem_soup(self.year, self.day)
        n_parts_solved = len(re.findall('Your puzzle answer was', soup.text))
        if n_parts_solved >= 2:
            print('Problem already solved!')
            return
        full_input = _get_full_input(self.year, self.day)
        answer = str(self.part1(full_input)) if n_parts_solved == 0 else str(self.part2(full_input))
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
