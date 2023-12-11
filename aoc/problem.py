import re
from abc import abstractmethod
from typing import Any


class Problem:
    def __init__(self) -> None:
        year, day = re.findall('\d+', self.__class__.__name__)
        self.year, self.day = int(year), int(day)

    @abstractmethod
    def part1(self, text: str, **kwargs) -> Any:
        pass

    @abstractmethod
    def part2(self, text: str, **kwargs) -> Any:
        pass
