from abc import abstractmethod
from typing import Any


class Problem:
    @abstractmethod
    def part1(self, text: str, **kwargs) -> Any:
        pass

    @abstractmethod
    def part2(self, text: str, **kwargs) -> Any:
        pass
