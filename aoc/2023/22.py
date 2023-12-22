from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, NamedTuple, Optional, Set


class Position3D(NamedTuple):
    x: int
    y: int
    z: int

    @staticmethod
    def from_str(s: str) -> 'Position3D':
        return Position3D(*map(int, s.split(',')))


@dataclass(frozen=True, eq=True)
class Brick:
    start: Position3D
    end: Position3D

    def move_down(self) -> Optional['Brick']:
        return (
            Brick(
                start=Position3D(self.start.x, self.start.y, self.start.z - 1),
                end=Position3D(self.end.x, self.end.y, self.end.z - 1),
            )
            if self.start.z > 1 and self.end.z > 1
            else None
        )

    def intersects(self, other: 'Brick') -> bool:
        for index in range(3):
            xi, yi, zi = index, (index + 1) % 3, (index + 2) % 3
            if (
                self.start[xi] == self.end[xi] == other.start[xi] == other.end[xi]
                and self.end[yi] >= other.start[yi]
                and self.start[yi] <= other.end[yi]
                and self.end[zi] >= other.start[zi]
                and self.start[zi] <= other.end[zi]
            ):
                return True

        return False

    @staticmethod
    def from_str(s: str) -> 'Brick':
        return Brick(*sorted(map(lambda x: Position3D.from_str(x), s.split('~'))))


def get_intersection(brick, other_bricks):
    return {
        other_brick for other_brick in other_bricks if brick.intersects(other_brick)
    }


def get_settled_bricks(text):
    bricks = [Brick.from_str(line) for line in text.splitlines()]

    settled_bricks = []
    for brick in sorted(bricks, key=lambda b: min(b.start.z, b.end.z)):
        while (down_brick := brick.move_down()) and not get_intersection(
            down_brick, settled_bricks
        ):
            brick = down_brick
        settled_bricks.append(brick)
    return settled_bricks


def part1(text):
    settled_bricks = get_settled_bricks(text)
    support_bricks = set()
    for index, brick in enumerate(settled_bricks):
        if not (down_brick := brick.move_down()):
            continue
        intersection = get_intersection(
            down_brick, settled_bricks[:index] + settled_bricks[index + 1 :]
        )
        if len(intersection) == 1:
            support_bricks.add(intersection.pop())
    return len(settled_bricks) - len(support_bricks)


def part2(text):
    settled_bricks = get_settled_bricks(text)
    graph = defaultdict(list)
    for index, brick in enumerate(settled_bricks):
        if not (down_brick := brick.move_down()):
            continue
        for support_brick in get_intersection(
            down_brick, settled_bricks[:index] + settled_bricks[index + 1 :]
        ):
            graph[support_brick].append(brick)

    n_total_falls = 0
    for removed_node in list(graph):
        in_degree = defaultdict(int)
        for next_nodes in graph.values():
            for next_node in next_nodes:
                in_degree[next_node] += 1

        zero_in_degree_nodes = [removed_node]
        n_falls = 0
        while len(zero_in_degree_nodes) > 0:
            node = zero_in_degree_nodes.pop()
            for next_node in graph[node]:
                in_degree[next_node] -= 1
                if in_degree[next_node] == 0:
                    n_falls += 1
                    zero_in_degree_nodes.append(next_node)
        n_total_falls += n_falls

    return n_total_falls
