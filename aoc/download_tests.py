import os
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List

import click
import yaml

from aoc.api import get_problem_soup


@dataclass(frozen=True)
class TestCase:
    input: str
    answer: str


def get_tests(year: int, day: int) -> List[TestCase]:
    soup = get_problem_soup(year, day)
    parts = soup.find_all('article')
    # assert len(parts) == 2
    test_cases = []
    for part in parts:
        text = soup.find_all('pre')[0].text
        if text.endswith('\n'):
            text = text[:-1]
        answer = [em.text for code in part.find_all('code') if (em := code.find('em'))][
            -1
        ]
        test_cases.append(TestCase(text, answer))
    return test_cases


def str_presenter(dumper, data):
    """configures yaml for dumping multiline strings
    Ref: https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data
    """
    if data.count('\n') > 0:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


yaml.add_representer(str, str_presenter)
now = datetime.now()


@click.command()
@click.option('--year', '-y', default=now.year)
@click.option('--day', '-d', default=now.day)
def main(year: int, day: int):
    test_config_path = f'{os.path.dirname(__file__)}/{year}/tests/{day:02d}.yml'
    test_data = {}
    if os.path.exists(test_config_path):
        with open(test_config_path) as f:
            test_data = yaml.safe_load(f)
    modified = False
    test_cases = get_tests(year, day)
    if 'part1' not in test_data:
        test_data['part1'] = [asdict(test_cases[0])]
        modified = True
    if 'part2' not in test_data and len(test_cases) > 1:
        test_data['part2'] = [asdict(test_cases[1])]
        modified = True

    if modified:
        with open(test_config_path, 'w') as f:
            yaml.dump(test_data, f, sort_keys=False)
        print(f'Test added to {test_config_path}')


if __name__ == '__main__':
    main()
