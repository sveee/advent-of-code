import os
import re
from abc import abstractmethod
from typing import Any, List

import requests
from bs4 import BeautifulSoup

SESSION = os.environ.get('SESSION')


def _get_problem_soup(year: int, day: int) -> str:
    return BeautifulSoup(
        requests.get(
            f'https://adventofcode.com/{year}/day/{day}',
            cookies=dict(session=SESSION),
        ).text,
        features='html.parser',
    )


def _get_full_input(year: int, day: int) -> str:
    input_text = requests.get(
        f'https://adventofcode.com/{year}/day/{day}/input',
        cookies=dict(session=SESSION),
    ).text
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
        self.part1, self.part2 = None, None

    @abstractmethod
    def solve_input(self, text: str) -> None:
        pass

    def solve(self) -> None:
        self.solve_input(_get_full_input(self.year, self.day))
        print(self.part1)
        print(self.part2)

    def test(self, test_index1: int = 0, test_index2: int = 0):
        values = []
        self.solve_input(_get_test_input(self.year, self.day, test_index1))
        values.append(self.part1)
        if self.part2 is not None:
            self.solve_input(_get_test_input(self.year, self.day, test_index2))
            values.append(self.part2)
        test_answers = _get_test_answers(self.year, self.day)
        for answer, value in zip(test_answers, values):
            if value is not None:
                print(_equal_status(str(value), answer))

    def submit(self) -> None:
        soup = _get_problem_soup(self.year, self.day)
        n_parts_solved = len(re.findall('Your puzzle answer was', soup.text))
        if n_parts_solved >= 2:
            print('Problem already solved!')
            return

        self.solve()
        answer = self.part1 if n_parts_solved == 0 else self.part2
        if answer is None:
            return

        soup = BeautifulSoup(
            requests.post(
                f'https://adventofcode.com/{self.year}/day/{self.day}/answer',
                data=dict(
                    level=n_parts_solved + 1,
                    answer=answer,
                ),
                cookies=dict(session=SESSION),
            ).text,
            features='html.parser',
        )
        print(re.sub('\s+', ' ', soup.find('article').text))
