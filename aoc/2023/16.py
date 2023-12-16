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


def get_n_energized(start_beam, grid):
    n, m = len(grid), len(grid[0])

    active_beams = [start_beam]
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



def part1(text):
    grid = text.splitlines()
    return get_n_energized(Beam(Pair(0, 0), Pair(0, 1)), grid)


def part2(text):
    start_beams = []
    grid = text.splitlines()
    n, m = len(grid), len(grid[0])
    for y in range(m):
        start_beams.append(Beam(Pair(0, y), Pair(1, 0)))
        start_beams.append(Beam(Pair(n-1, y), Pair(-1, 0)))
    for x in range(n):
        start_beams.append(Beam(Pair(x, 0), Pair(0, 1)))
        start_beams.append(Beam(Pair(x, m-1), Pair(0, -1)))
    return max(get_n_energized(start_beam, grid) for start_beam in start_beams)
