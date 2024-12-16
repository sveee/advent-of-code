from dataclasses import dataclass
from queue import PriorityQueue


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True, order=True)
class State:
    position: Point
    direction: Point


directions = [
    Point(-1, 0),
    Point(1, 0),
    Point(0, -1),
    Point(0, 1),
]


def part1(text):
    grid = text.splitlines()
    s = next(
        Point(x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == 'S'
    )
    start_state = State(s, Point(0, 1))
    queue = PriorityQueue()
    queue.put((0, start_state))
    visited = {start_state}

    while not queue.empty():
        priority, state = queue.get()

        if grid[state.position.x][state.position.y] == 'E':
            return priority

        for direction in directions:
            if (next_state := State(state.position, direction)) not in visited:
                queue.put((priority + 1000, next_state))
                visited.add(next_state)

        next_position = Point(
            state.position.x + state.direction.x, state.position.y + state.direction.y
        )

        if grid[next_position.x][next_position.y] != '#':
            next_state = State(next_position, state.direction)
            queue.put((priority + 1, next_state))
            visited.add(next_state)

    raise


def part2(text):
    pass
