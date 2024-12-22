from typing import Any, Dict

import requests
from bs4 import BeautifulSoup


class AOCApi:
    def __init__(self, session_id: str) -> None:
        self._session_id = session_id

    def get_request(self, url: str) -> str:
        return requests.get(
            url,
            cookies=dict(session=self._session_id),
        ).text

    def post_request(self, url: str, data: Dict[str, Any]) -> str:
        return requests.post(
            url,
            data=data,
            cookies=dict(session=self._session_id),
        ).text

    def get_problem_input_data(self, year: int, day: int) -> str:
        input_text = self.get_request(
            f'https://adventofcode.com/{year}/day/{day}/input'
        )
        if input_text.endswith('\n'):
            input_text = input_text[:-1]
        return input_text

    def submit_solution(self, answer: str, level: int, year: int, day: int) -> str:
        return self.post_request(
            f'https://adventofcode.com/{year}/day/{day}/answer',
            {'level': level, 'answer': answer},
        )

    def get_problem_soup(self, year: int, day: int) -> str:
        return BeautifulSoup(
            self.get_request(f'https://adventofcode.com/{year}/day/{day}'),
            features='html.parser',
        )
