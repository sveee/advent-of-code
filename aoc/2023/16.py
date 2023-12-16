from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Pair:
    x: int
    y: int


@dataclass(frozen=True, eq=True)
class Beam:
    position: Pair
    direction: Pair


forward_slash_map = {Pair(-1, 0): Pair(-1, 0)}


def part1(text):
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])

    active_beams = [Beam(Pair(0, 0), Pair(0, 1))]
    energized = set()
    visited = set()
    while len(active_beams) > 0:
        beam = active_beams.pop()
        if beam in visited:
            continue

        visited.add(beam)
        if not (0 <= beam.position.x < n and 0 <= beam.position.y < m):
            continue

        energized.add(beam.position)
        next_directions = []
        if grid[beam.position.x][beam.position.y] == '|':
            if beam.direction.x == 0:
                next_directions.extend([Pair(-1, 0), Pair(1, 0)])
            else:
                next_directions.append(beam.direction)
        elif grid[beam.position.x][beam.position.y] == '-':
            if beam.direction.y == 0:
                next_directions.extend([Pair(0, -1), Pair(0, 1)])
            else:
                next_directions.append(beam.direction)
        elif grid[beam.position.x][beam.position.y] == '/':
            next_directions.append(Pair(-beam.direction.y, -beam.direction.x))
        elif grid[beam.position.x][beam.position.y] == '\\':
            next_directions.append(Pair(beam.direction.y, beam.direction.x))
        elif grid[beam.position.x][beam.position.y] == '.':
            next_directions.append(beam.direction)

        for next_direction in next_directions:
            active_beams.append(
                Beam(
                    Pair(beam.position.x + next_direction.x,
                    beam.position.y + next_direction.y),
                    next_direction
                ),
            )

    return len(energized)


def part2(text):
    pass
