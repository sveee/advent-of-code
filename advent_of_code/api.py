import os
from typing import Any, Dict

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


def get_full_input(year: int, day: int) -> str:
    input_text = get_request(f'https://adventofcode.com/{year}/day/{day}/input')
    if input_text.endswith('\n'):
        input_text = input_text[:-1]
    return input_text


def submit_solution(answer: str, level: int, year: int, day: int):
    post_request(
        f'https://adventofcode.com/{year}/day/{day}/answer',
        {'level': level, 'answer': answer},
    )


def get_problem_soup(year: int, day: int) -> str:
    return BeautifulSoup(
        get_request(f'https://adventofcode.com/{year}/day/{day}'),
        features='html.parser',
    )
