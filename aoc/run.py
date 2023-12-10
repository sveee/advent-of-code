import inspect
import os
from datetime import datetime
from importlib import import_module
from typing import Any

import click
import yaml

now = datetime.now()


def _equal_status(generated: Any, expected: Any) -> str:
    return (
        f'✅ {generated} == {expected}'
        if generated == expected
        else f'❌ {generated} != {expected}'
    )


@click.command()
@click.option('--year', '-y', default=now.year)
@click.option('--day', '-d', default=now.day)
def main(year: int, day: int):
    problem_module = import_module(f'aoc.{year}.{day:02d}')
    problem = getattr(problem_module, f'Problem{year}_{day:02d}')()
    test_config_path = f'{os.path.dirname(__file__)}/{year}/tests/{day:02d}.yml'
    with open(test_config_path) as f:
        test_data = yaml.safe_load(f)

    for part in ['part1', 'part2']:
        if part in test_data:
            print(part)
            for test_index, test_case in enumerate(test_data[part]):
                # print(inspect.getsource(getattr(problem, part)))
                generated = str(getattr(problem, part)(test_case['input']))
                excepted = str(test_case['answer'])
                print(f'test{test_index}:', _equal_status(generated, excepted))


if __name__ == '__main__':
    main()
