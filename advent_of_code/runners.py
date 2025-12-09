import os
import subprocess
import tempfile
from abc import ABC, abstractmethod
from importlib import import_module
from typing import Any

from advent_of_code.types import Language, Part


def run_with_live_output(
    command: list[str], check: bool = True, live_output: False = False
) -> str:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Merge stderr into stdout
        text=True,
        bufsize=1,
    )

    output_lines = []

    for line in process.stdout:
        if live_output:
            print(line, end='')
        output_lines.append(line)

    return_code = process.wait()
    stdout_text = ''.join(output_lines)
    if check and return_code != 0:
        raise subprocess.CalledProcessError(return_code, command, stdout_text)
    return stdout_text


class Runner(ABC):
    def __init__(self, year: int, day: int, live_output: bool) -> None:
        self.year = year
        self.day = day
        self.live_output = live_output

    @abstractmethod
    def run(self, part: Part, input_data: str, **kwargs: Any) -> str: ...


class PythonRunner(Runner):
    def __init__(self, year: int, day: int, live_output: bool) -> None:
        super().__init__(year, day, live_output)

    def run(self, part: Part, input_data: str, **kwargs: Any) -> str:
        module = import_module(f'advent_of_code.{self.year}.python.{self.day:02d}')
        part_func = getattr(module, part.value, None)
        return str(part_func(input_data, **kwargs))


class CompiledRunner(Runner):
    binary_path: str

    def __init__(self, year: int, day: int, live_output: bool) -> None:
        super().__init__(year, day, live_output)

    def run(self, part: Part, input_data: str, **kwargs: Any) -> str:
        try:
            if not os.path.exists(self.binary_path):
                return ''
            with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tmp_file:
                tmp_file.write(input_data)
                tmp_file.flush()
                command = [self.binary_path, part.value, tmp_file.name]
                result = run_with_live_output(command, live_output=self.live_output)
            return result.strip().splitlines()[-1]
        except subprocess.CalledProcessError as e:
            print(f'Error running binary: {e}')
            print(f'stderr: {e.stderr}')
            return ''


class RustRunner(CompiledRunner):
    def __init__(self, year: int, day: int, live_output: bool) -> None:
        super().__init__(year, day, live_output)
        self.binary_path = os.path.join(
            os.path.join(os.path.dirname(__file__), '..', 'advent_of_code'),
            f'{year}/rust/target/debug/{day:02d}',
        )
        assert os.path.exists(self.binary_path), f'{self.binary_path} does not exist'


class CPPRunner(CompiledRunner):
    def __init__(self, year: int, day: int, live_output: bool) -> None:
        super().__init__(year, day, live_output)
        self.binary_path = os.path.join(
            os.path.join(os.path.dirname(__file__), '..', 'advent_of_code'),
            f'{year}/cpp/bin/{day:02d}',
        )


language_runner_map = {
    Language.PYTHON: PythonRunner,
    Language.RUST: RustRunner,
    Language.CPP: CPPRunner,
}
