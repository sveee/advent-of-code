import os
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml
from bs4 import BeautifulSoup

from advent_of_code.api import AOCApi
from advent_of_code.runners import Runner, language_runner_map
from advent_of_code.types import Language, Part


def _open_file(file_path) -> None:
    subprocess.run(['code', file_path], capture_output=True)


def _configure_yaml_multiline_dump() -> None:
    """Configures YAML to use the '|' style for multiline strings."""

    def str_presenter(dumper, data):
        if data.count('\n') > 0:  # Check for multiline string
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    yaml.add_representer(str, str_presenter)


@dataclass(frozen=True)
class _TestCase:
    input: str
    answer: str


class ProblemSolver:
    GREEN = '\033[92m'
    RESET = '\033[0m'

    def __init__(
        self, language: Language, year: int, day: int, session_id: str
    ) -> None:
        self.runner: Runner = language_runner_map[language](year, day)
        self.language = language
        self.year = year
        self.day = day
        self.test_data = {}
        self.aoc_api = AOCApi(session_id)
        self.input_data_path = Path(
            f'{os.path.dirname(__file__)}/../advent_of_code/'
            f'{self.year}/input/{self.day:02d}.txt'
        )

    @staticmethod
    def _equal_status(generated: Any, expected: Any) -> str:
        return (
            f'✅ {generated} == {expected}'
            if generated == expected
            else f'❌ {generated} != {expected}'
        )

    def test_pass(self, test_index: int, part: Part, test_case: dict[str, Any]) -> bool:
        input_data = test_case.pop('input')
        expected_output = str(test_case.pop('answer'))
        parameters = test_case
        generated_output = self.runner.run(part, input_data, **parameters)
        status = self._equal_status(generated_output, expected_output)
        print(f'test {part.value}.{test_index}: {status}')
        return generated_output == expected_output

    def all_tests_pass(self) -> bool:
        for part in Part:
            if part.value in self.test_data:
                for test_index, test_case in enumerate(
                    self.test_data[part.value] if self.test_data[part.value] else [],
                    start=1,
                ):
                    if not self.test_pass(test_index, part, test_case):
                        return False
        return True

    def fetch_existing_answers(self) -> dict[Part, str]:
        soup = self.aoc_api.get_problem_soup(self.year, self.day)
        answer_ps = soup.find_all('p')
        answers = [
            p.find('code').text
            for p in answer_ps
            if p.text.startswith('Your puzzle answer was')
        ]
        return {part: answer for part, answer in zip([Part.PART1, Part.PART2], answers)}

    def get_problem_input(self) -> str:
        if not os.path.exists(self.input_data_path):
            self.input_data_path.parent.mkdir(parents=True, exist_ok=True)
            input_data = self.aoc_api.get_problem_input_data(self.year, self.day)
            self.input_data_path.write_text(input_data)
            _open_file(self.input_data_path)
        else:
            input_data = self.input_data_path.read_text()
        return input_data

    def display_solutions(self, answers: dict[Part, str]) -> None:
        print('Problem already solved!')
        problem_input = self.get_problem_input()
        for part in Part:
            answer = self.runner.run(part, problem_input)
            print(
                f'{part.value}:',
                (
                    answer
                    if answer == answers[part]
                    else self._equal_status(answer, answers[part])
                ),
            )

    def submit_and_display_response(self, answer: str, level: int) -> None:
        response = self.aoc_api.submit_solution(
            answer=answer,
            level=level,
            year=self.year,
            day=self.day,
        )
        soup = BeautifulSoup(response, features='html.parser')
        response = re.sub(r'\s+', ' ', soup.find('article').text)
        status = '✅' if response.startswith('That\'s the right answer!') else '❌'
        print(status)
        print(response)

    def _create_solution_file(self) -> None:
        """Creates the Python file for the given day if it doesn't exist."""
        if self.language == Language.PYTHON:
            python_file_path = Path(
                f'{os.path.dirname(__file__)}/../advent_of_code/{self.year}/python/{self.day:02d}.py'
            )
            if not python_file_path.exists():
                python_file_path.parent.mkdir(parents=True, exist_ok=True)
                python_file_path.write_text(
                    '\ndef part1(text):\n    pass\n\ndef part2(text):\n    pass\n'
                )
                _open_file(str(python_file_path))

    def _get_tests(self) -> list[_TestCase]:
        """Fetches test cases for the given year and day."""
        soup = self.aoc_api.get_problem_soup(self.year, self.day)
        test_cases = []
        for part in soup.find_all('article'):
            pres = part.find_all('pre') or soup.find_all('pre')
            if not pres:
                continue
            input_text = pres[0].text.rstrip()

            codes = part.find_all('code') or soup.find_all('code')
            code_ems = [em.text for code in codes if (em := code.find('em'))]
            codes = [code.text for code in codes]
            assert code_ems or codes
            answer_text = code_ems[-1] if code_ems else codes[-1]
            test_cases.append(_TestCase(input_text, answer_text))
        return test_cases

    def _create_tests_file(self) -> None:
        test_config_path = Path(
            f'{os.path.dirname(__file__)}/../advent_of_code/{self.year}/tests/{self.day:02d}.yml'
        )
        os.makedirs(test_config_path.parent, exist_ok=True)
        # Load existing test data if the file exists
        test_case = {}
        first_time = True
        if test_config_path.exists():
            first_time = False
            with open(test_config_path) as f:
                test_data = yaml.safe_load(f) or {}

        # Fetch test cases from the problem
        test_cases = self._get_tests()

        # Update test data
        for part, test_case in zip(['part1', 'part2'], test_cases):
            if part not in test_data:
                test_data[part] = [asdict(test_case)]

        # Write updated test data to YAML file
        _configure_yaml_multiline_dump()
        if test_data:
            test_config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(test_config_path, 'w') as f:
                yaml.dump(test_data, f, sort_keys=False)
            if first_time:
                _open_file(test_config_path)
        self.test_data = test_data

    def solve(self) -> None:
        problem_input = self.get_problem_input()
        self._create_solution_file()
        self._create_tests_file()
        print(f'{self.GREEN}[Test]{self.RESET}')
        if not self.all_tests_pass():
            return
        print(f'{self.GREEN}[Submit]{self.RESET}')
        answers = self.fetch_existing_answers()
        if len(answers) == 2:
            self.display_solutions(answers)
        else:
            answer_to_submit = self.runner.run(
                Part.PART1 if len(answers) == 0 else Part.PART2,
                problem_input,
            )
            level = len(answers) + 1
            self.submit_and_display_response(answer=answer_to_submit, level=level)
