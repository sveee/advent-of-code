import os
import re
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from importlib import import_module
from typing import Any

import click
import yaml
from bs4 import BeautifulSoup

from advent_of_code.api import get_full_input, get_problem_soup, submit_solution

now = datetime.now()


class Solution(Enum):
    PART1 = 'part1'
    PART2 = 'part2'


class Runner(ABC):
    def __init__(self, year: int, day: int) -> None:
        self.year = year
        self.day = day

    @abstractmethod
    def run(self, part: Solution, input_data: str, **kwargs: Any) -> str: ...


class PythonRunner(Runner):
    def __init__(self, year: int, day: int):
        super().__init__(year, day)
        self.module = import_module(f'advent_of_code.{year}.python.{day:02d}')

    def run(self, part: Solution, input_data: str, **kwargs: Any) -> str:
        part_func = getattr(self.module, part.value, None)
        return str(part_func(input_data, **kwargs))


class ProblemSolver:
    def __init__(self, runner: Runner):
        self.runner = runner
        self.test_data = self.read_test_data()

    def read_test_data(self) -> dict[str, Any]:
        test_folder = os.path.join(
            os.path.dirname(__file__), str(self.runner.year), 'tests'
        )
        os.makedirs(test_folder, exist_ok=True)
        test_config_path = os.path.join(test_folder, f'{self.runner.day:02d}.yml')
        with open(test_config_path, 'r') as file:
            test_data = yaml.safe_load(file)
        return test_data

    @staticmethod
    def _equal_status(generated: Any, expected: Any) -> str:
        return (
            f'✅ {generated} == {expected}'
            if generated == expected
            else f'❌ {generated} != {expected}'
        )

    def run_test(self, part: Solution, test_case: dict[str, Any]) -> bool:
        input_data = test_case.pop('input')
        expected_output = str(test_case.pop('answer'))
        parameters = test_case
        generated_output = self.runner.run(part, input_data, **parameters)
        status = self._equal_status(generated_output, expected_output)
        print(f'Test: {status}')
        return generated_output == expected_output

    def check_all_tests(self) -> bool:
        all_tests_pass = True
        for part in Solution:
            if part.value in self.test_data:
                print(f'Running tests for {part.value}')
                for test_index, test_case in enumerate(
                    self.test_data[part.value], start=1
                ):
                    print(f'Test {test_index}:')
                    all_tests_pass &= self.run_test(part, test_case)
        return all_tests_pass

    def get_n_parts_solved(self) -> int:
        soup = get_problem_soup(self.runner.year, self.runner.day)
        n_parts_solved = len(re.findall('Your puzzle answer was', soup.text))
        return n_parts_solved

    def display_solutions(self):
        print('Problem already solved!')
        full_input = get_full_input(self.runner.year, self.runner.day)
        for part in Solution:
            print(f'{part.value}:', self.runner.run(part, full_input))

    def get_solution_answer(self) -> str:
        full_input = get_full_input(self.runner.year, self.runner.day)
        n_parts_solved = self.get_n_parts_solved()
        if n_parts_solved == 0:
            return self.runner.run(Solution.PART1, full_input)
        return self.runner.run(Solution.PART2, full_input)

    def submit_and_display_response(self, answer: str) -> None:
        response = submit_solution(
            answer=answer,
            level=self.get_n_parts_solved() + 1,
            year=self.runner.year,
            day=self.runner.day,
        )
        soup = BeautifulSoup(response, features='html.parser')
        print(re.sub(r'\s+', ' ', soup.find('article').text))

    def solve(self) -> None:
        if not self.check_all_tests():
            return
        if self.get_n_parts_solved() >= 2:
            self.display_solutions()
            return
        answer = self.get_solution_answer()
        if not answer:
            return
        self.submit_and_display_response(answer)


@click.command()
@click.option('--year', '-y', default=now.year, help='Year of the problem')
@click.option('--day', '-d', default=now.day, help='Day of the problem')
def main(year: int, day: int) -> None:
    runner = PythonRunner(year, day)
    solver = ProblemSolver(runner)
    solver.solve()


if __name__ == '__main__':
    main()
