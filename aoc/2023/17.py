from dataclasses import dataclass
from queue import PriorityQueue


@dataclass(frozen=True, eq=True)
class Node:
    x: int
    y: int
    last_direction: str
    n_blocks: int

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


directions = {
    'north': (-1, 0),
    'south': (1, 0),
    'west': (0, -1),
    'east': (0, 1),
}
opposite_directions = {
    'north': 'south',
    'south': 'north',
    'west': 'east',
    'east': 'west',
}


def get_neighbours(node, grid, min_n_blocks, max_m_blocks):
    neighbours = []
    for direction, (dx, dy) in directions.items():
        if direction == opposite_directions.get(node.last_direction):
            # we cannot go in the direction we came from
            continue
        if (
            node.n_blocks < min_n_blocks
            and node.last_direction in directions
            and direction != node.last_direction
        ):
            # we need to go in a certain direction at least min_n_blocks times
            continue
        if node.n_blocks == max_m_blocks and node.last_direction == direction:
            # we need to go in a certain direction at most max_m_blocks times
            continue
        nx, ny = node.x + dx, node.y + dy
        if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
            continue
        neighbours.append(
            Node(
                nx,
                ny,
                direction,
                node.n_blocks + 1 if node.last_direction == direction else 1,
            )
        )
    return neighbours


def get_least_heat_loss(grid, min_n_blocks, max_m_blocks):
    # Dijkstra
    pq = PriorityQueue()
    pq.put((0, Node(0, 0, '', 0)))
    minimal_heat_loss = {}
    while not pq.empty():
        current_heat_loss, node = pq.get()
        for next_node in get_neighbours(node, grid, min_n_blocks, max_m_blocks):
            if next_node not in minimal_heat_loss:
                minimal_heat_loss[next_node] = current_heat_loss + int(
                    grid[next_node.x][next_node.y]
                )
                pq.put((minimal_heat_loss[next_node], next_node))

    return min(
        heat_loss
        for node, heat_loss in minimal_heat_loss.items()
        if node.x == len(grid) - 1 and node.y == len(grid[0]) - 1
    )


def part1(text):
    grid = text.splitlines()
    return get_least_heat_loss(grid, 0, 3)


def part2(text):
    grid = text.splitlines()
    return get_least_heat_loss(grid, 4, 10)
