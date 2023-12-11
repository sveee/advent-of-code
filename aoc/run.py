import os
import re
from datetime import datetime
from importlib import import_module
from typing import Any

import click
import yaml
from bs4 import BeautifulSoup

from aoc.api import get_full_input, get_problem_soup, post_request
from aoc.problem import Problem

now = datetime.now()


def _equal_status(generated: Any, expected: Any) -> str:
    return (
        f'✅ {generated} == {expected}'
        if generated == expected
        else f'❌ {generated} != {expected}'
    )


def submit(problem: Problem, year: int, day: int) -> None:
    soup = get_problem_soup(year, day)
    n_parts_solved = len(re.findall('Your puzzle answer was', soup.text))
    if n_parts_solved >= 2:
        print('Problem already solved!')
        return
    full_input = get_full_input(year, day)
    answer = (
        str(problem.part1(full_input))
        if n_parts_solved == 0
        else str(problem.part2(full_input))
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
    problem = getattr(problem_module, f'Problem{year}_{day:02d}')()
    test_config_path = f'{os.path.dirname(__file__)}/{year}/tests/{day:02d}.yml'
    with open(test_config_path) as f:
        test_data = yaml.safe_load(f)

    all_tests_pass = True
    for part in ['part1', 'part2']:
        if part in test_data:
            print(part)
            for test_index, test_case in enumerate(test_data[part]):
                text_input, excepted = test_case.pop('input'), str(
                    test_case.pop('answer')
                )
                parameters = test_case
                generated = str(getattr(problem, part)(text_input, **parameters))
                print(f'test{test_index}:', _equal_status(generated, excepted))
                all_tests_pass &= generated == excepted

    if all_tests_pass:
        submit(problem, year, day)


if __name__ == '__main__':
    main()
