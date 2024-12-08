from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Segment(NamedTuple):
    start: Point
    step: Point
    steps: int


class Intersection(NamedTuple):
    point: Point
    steps: int


direction_map = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1),
}


def get_wire_segments(path):
    x, y, s = 0, 0, 0
    segments = []
    for step in path.split(','):
        dir, size = step[0], int(step[1:])
        dx, dy = direction_map[dir]
        dx, dy = size * dx, size * dy
        segments.append(Segment(Point(x, y), Point(dx, dy), s))
        x, y, s = x + dx, y + dy, s + abs(dx) + abs(dy)
    return segments


def get_intersection(segment1: Segment, segment2: Segment):
    if (segment1.step.x != 0) == (segment2.step.x != 0):
        return None

    if segment2.step.y == 0:
        segment1, segment2 = segment2, segment1

    assert segment1.step.y == 0

    start_x, end_x = segment1.start.x, segment1.start.x + segment1.step.x
    if start_x > end_x:
        start_x, end_x = end_x, start_x

    start_y, end_y = segment2.start.y, segment2.start.y + segment2.step.y
    if start_y > end_y:
        start_y, end_y = end_y, start_y

    if not (start_x < segment2.start.x < end_x and start_y < segment1.start.y < end_y):
        return None

    return Intersection(
        Point(segment2.start.x, segment1.start.y),
        segment1.steps
        + abs(segment1.start.x - segment2.start.x)
        + segment2.steps
        + abs(segment2.start.y - segment1.start.y),
    )


def part1(text):
    wire_path1, wire_path2 = text.splitlines()
    wire_segments1 = get_wire_segments(wire_path1)
    wire_segments2 = get_wire_segments(wire_path2)
    return min(
        abs(intersection.point.x) + abs(intersection.point.y)
        for segment1 in wire_segments1
        for segment2 in wire_segments2
        if (intersection := get_intersection(segment1, segment2))
    )


def part2(text):
    wire_path1, wire_path2 = text.splitlines()
    wire_segments1 = get_wire_segments(wire_path1)
    wire_segments2 = get_wire_segments(wire_path2)
    return min(
        intersection.steps
        for segment1 in wire_segments1
        for segment2 in wire_segments2
        if (intersection := get_intersection(segment1, segment2))
    )
