from collections import defaultdict
from queue import PriorityQueue
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class State(NamedTuple):
    position: Point
    direction: Point


DIRECTIONS = [
    Point(-1, 0),
    Point(1, 0),
    Point(0, -1),
    Point(0, 1),
]


def find_value(v, grid):
    return next(
        Point(x, y)
        for x in range(len(grid))
        for y in range(len(grid[0]))
        if grid[x][y] == v
    )


def dijkstra(s, grid):
    start_state = State(s, Point(0, 1))
    queue = PriorityQueue()
    queue.put((0, start_state))
    distance = {start_state: 0}
    prev = defaultdict(list)
    while not queue.empty():
        priority, state = queue.get()
        for direction in DIRECTIONS:
            next_state = State(state.position, direction)
            if next_state not in distance:
                distance[next_state] = priority + 1000
                queue.put((distance[next_state], next_state))
            if priority + 1000 == distance[next_state]:
                prev[next_state].append(state)

        next_position = Point(
            state.position.x + state.direction.x,
            state.position.y + state.direction.y,
        )
        if grid[next_position.x][next_position.y] != '#':
            next_state = State(next_position, state.direction)
            if next_state not in distance:
                distance[next_state] = priority + 1
                queue.put((distance[next_state], next_state))
            if priority + 1 == distance[next_state]:
                prev[next_state].append(state)

    return distance, prev


def part1(text):
    grid = text.splitlines()
    s = find_value('S', grid)
    e = find_value('E', grid)
    distance, _ = dijkstra(s, grid)
    return min(distance[State(e, direction)] for direction in DIRECTIONS)


def part2(text):
    grid = text.splitlines()
    s = find_value('S', grid)
    e = find_value('E', grid)
    distance, prev = dijkstra(s, grid)
    best_end_state = min(
        [State(e, direction) for direction in DIRECTIONS], key=lambda x: distance[x]
    )
    paths = {best_end_state}
    stack = [best_end_state]
    while len(stack) > 0:
        position = stack.pop()
        for next_position in prev[position]:
            if next_position not in paths:
                stack.append(next_position)
                paths.add(next_position)
    return len({state.position for state in paths})
