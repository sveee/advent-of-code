from dataclasses import dataclass, field
from typing import List

directions = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}


@dataclass(frozen=True)
class Instruction:
    direction: str
    steps: int


@dataclass(frozen=True)
class YSegment:
    start: int
    end: int
    x: int
    flips_y_parity: bool

    def size(self):
        return self.end - self.start + 1


@dataclass(frozen=True)
class XSegment:
    start: int
    end: int
    y: int

    def size(self):
        return self.end - self.start + 1


@dataclass
class Trench:
    x_segments: List[XSegment] = field(default_factory=list)
    y_segments: List[YSegment] = field(default_factory=list)

    def size(self):
        return sum(x_segment.size() - 1 for x_segment in self.x_segments) + sum(
            y_segment.size() - 1 for y_segment in self.y_segments
        )


def get_line_interior_size(segments):
    interior_size = 0
    is_inside = False
    for index in range(len(segments)):
        if is_inside:
            interior_size += segments[index].start - segments[index - 1].end - 1
        is_inside ^= segments[index].flips_y_parity
    return interior_size


def get_x_segments(trench):
    xs = sorted(
        {x for x_segment in trench.x_segments for x in [x_segment.start, x_segment.end]}
    )
    x_segments = []
    for index in range(len(xs)):
        x_segments.append(XSegment(xs[index], xs[index], 0))
        if index + 1 < len(xs):
            if xs[index] + 1 <= xs[index + 1] - 1:
                x_segments.append(XSegment(xs[index] + 1, xs[index + 1] - 1, 0))
    return x_segments


def get_y_segments(x, trench):
    y_segments = []
    for x_segment in trench.x_segments:
        if x_segment.start < x < x_segment.end:
            y_segments.append(
                YSegment(start=x_segment.y, end=x_segment.y, x=0, flips_y_parity=True)
            )
    for y_segment in trench.y_segments:
        if y_segment.x == x:
            y_segments.append(y_segment)
    return sorted(y_segments, key=lambda x: x.start)


def get_trench(instructions):
    x, y = 0, 0
    trench = Trench()
    n = len(instructions)
    for index in range(n):
        dx, dy = directions[instructions[index].direction]
        steps = instructions[index].steps
        if dy == 0:
            trench.x_segments.append(
                XSegment(start=min(x, x + steps * dx), end=max(x, x + steps * dx), y=y)
            )
        else:
            flips_y_parity = (
                instructions[(index - 1 + n) % n].direction
                == instructions[(index + 1 + n) % n].direction
            )
            trench.y_segments.append(
                YSegment(
                    start=min(y, y + steps * dy),
                    end=max(y, y + steps * dy),
                    x=x,
                    flips_y_parity=flips_y_parity,
                )
            )
        x, y = x + steps * dx, y + steps * dy
    return trench


def get_interior_size(trench):
    x_segments = get_x_segments(trench)
    interior_size = trench.size()
    for x_segment in x_segments:
        y_segments = get_y_segments(x_segment.start, trench)
        interior_size += x_segment.size() * get_line_interior_size(y_segments)
    return interior_size


def part1(text):
    instructions = []
    for line in text.splitlines():
        direction, steps, color = line.split()
        instructions.append(Instruction(direction, int(steps)))
    trench = get_trench(instructions)
    return get_interior_size(trench)


code_to_direction = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}


def part2(text):
    instructions = []
    for line in text.splitlines():
        _direction, _steps, color = line.split()
        instructions.append(
            Instruction(code_to_direction[color[-2]], int(color[2:-2], 16))
        )
    trench = get_trench(instructions)
    return get_interior_size(trench)
