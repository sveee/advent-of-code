import os
import subprocess
import tempfile
from abc import ABC, abstractmethod
from importlib import import_module
from typing import Any

from advent_of_code.types import Language, Part


class Runner(ABC):
    def __init__(self, year: int, day: int) -> None:
        self.year = year
        self.day = day

    @abstractmethod
    def run(self, part: Part, input_data: str, **kwargs: Any) -> str: ...


class PythonRunner(Runner):
    def __init__(self, year: int, day: int) -> None:
        super().__init__(year, day)
        self.module = import_module(f'advent_of_code.{year}.python.{day:02d}')

    def run(self, part: Part, input_data: str, **kwargs: Any) -> str:
        part_func = getattr(self.module, part.value, None)
        return str(part_func(input_data, **kwargs))


class RustRunner(Runner):
    def __init__(self, year: int, day: int) -> None:
        super().__init__(year, day)
        self.binary_path = os.path.join(
            os.path.join(os.path.dirname(__file__), '..', 'advent_of_code'),
            f'{year}/rust/target/debug/{day:02d}',
        )
        assert os.path.exists(self.binary_path), f'{self.binary_path} does not exist'

    def run(self, part: Part, input_data: str, **kwargs: Any) -> str:
        try:
            with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tmp_file:
                tmp_file.write(input_data)
                tmp_file.flush()
                result = subprocess.run(
                    [self.binary_path, part.value, tmp_file.name],
                    capture_output=True,
                    text=True,
                    check=True,
                )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f'Error running Rust binary: {e}')
            print(f'stderr: {e.stderr}')
            return ''


class CPPRunner(Runner):
    def __init__(self, year: int, day: int) -> None:
        super().__init__(year, day)
        self.binary_path = os.path.join(
            os.path.join(os.path.dirname(__file__), '..', 'advent_of_code'),
            f'{year}/cpp/bin/{day:02d}',
        )

    def run(self, part: Part, input_data: str, **kwargs: Any) -> str:
        try:
            if not os.path.exists(self.binary_path):
                return ''
            with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tmp_file:
                tmp_file.write(input_data)
                tmp_file.flush()
                result = subprocess.run(
                    [self.binary_path, part.value, tmp_file.name],
                    capture_output=True,
                    text=True,
                    check=True,
                )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f'Error running C++ binary: {e}')
            print(f'stderr: {e.stderr}')
            return ''


language_runner_map = {
    Language.PYTHON: PythonRunner,
    Language.RUST: RustRunner,
    Language.CPP: CPPRunner,
}
