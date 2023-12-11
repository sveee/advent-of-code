import os
import re
from datetime import datetime
from enum import Enum
from importlib import import_module
from typing import Any, Callable

import click
import yaml
from bs4 import BeautifulSoup

from aoc.api import get_full_input, get_problem_soup, post_request

now = datetime.now()


class Solution(Enum):
    PART1 = 'part1'
    PART2 = 'part2'


def _equal_status(generated: Any, expected: Any) -> str:
    return (
        f'✅ {generated} == {expected}'
        if generated == expected
        else f'❌ {generated} != {expected}'
    )


def submit(solution_funcs: Callable[[Solution], Any], year: int, day: int) -> None:
    soup = get_problem_soup(year, day)
    n_parts_solved = len(re.findall('Your puzzle answer was', soup.text))
    if n_parts_solved >= 2:
        print('Problem already solved!')
        return
    full_input = get_full_input(year, day)
    answer = (
        str(solution_funcs[Solution.PART1](full_input))
        if n_parts_solved == 0
        else str(solution_funcs[Solution.PART2](full_input))
    )
    if answer is None:
        return
    soup = BeautifulSoup(
        post_request(
            f'https://adventofcode.com/{year}/day/{day}/answer',
            dict(
                level=n_parts_solved + 1,
                answer=answer,
            ),
        ),
        features='html.parser',
    )
    print(re.sub('\s+', ' ', soup.find('article').text))


@click.command()
@click.option('--year', '-y', default=now.year)
@click.option('--day', '-d', default=now.day)
def main(year: int, day: int) -> None:
    problem_module = import_module(f'aoc.{year}.{day:02d}')
    test_config_path = f'{os.path.dirname(__file__)}/{year}/tests/{day:02d}.yml'
    with open(test_config_path) as f:
        test_data = yaml.safe_load(f)

    solution_funcs = {}
    for part in Solution:
        solution_funcs[part] = getattr(problem_module, part.value)

    all_tests_pass = True
    for part in Solution:
        if part.value in test_data:
            print(part.value)
            for test_index, test_case in enumerate(test_data[part.value]):
                text_input, excepted = test_case.pop('input'), str(
                    test_case.pop('answer')
                )
                parameters = test_case
                generated = str(solution_funcs[part](text_input, **parameters))
                print(f'test{test_index}:', _equal_status(generated, excepted))
                assert generated == excepted
                all_tests_pass &= generated == excepted

    if all_tests_pass:
        submit(solution_funcs, year, day)


if __name__ == '__main__':
    main()
