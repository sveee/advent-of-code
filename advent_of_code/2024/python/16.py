from collections import defaultdict
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
            if next_state not in visited:
                queue.put((priority + 1, next_state))
                visited.add(next_state)


def find_value(v, grid):
    return next(
        Point(x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == v
    )


def part2(text):
    grid = text.splitlines()
    s = find_value('S', grid)
    e = find_value('E', grid)
    start_state = State(s, Point(0, 1))
    queue = PriorityQueue()
    queue.put((0, start_state))
    visited = {start_state: 0}
    prev = defaultdict(list)

    while not queue.empty():
        priority, state = queue.get()
        for direction in directions:
            next_state = State(state.position, direction)
            if next_state not in visited:
                visited[next_state] = priority + 1000
                queue.put((visited[next_state], next_state))
            if priority + 1000 == visited[next_state]:
                prev[next_state].append(state)

        next_position = Point(
            state.position.x + state.direction.x,
            state.position.y + state.direction.y,
        )
        if grid[next_position.x][next_position.y] != '#':
            next_state = State(next_position, state.direction)
            if next_state not in visited:
                visited[next_state] = priority + 1
                queue.put((visited[next_state], next_state))
            if priority + 1 == visited[next_state]:
                prev[next_state].append(state)

    end_states = [State(e, direction) for direction in directions]
    best_end_state = min(end_states, key=lambda x: visited[x])
    paths = {best_end_state}
    stack = [best_end_state]
    while len(stack) > 0:
        position = stack.pop()
        for next_position in prev[position]:
            if next_position not in paths:
                stack.append(next_position)
                paths.add(next_position)

    return len({state.position for state in paths})
