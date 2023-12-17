
from dataclasses import dataclass
from queue import PriorityQueue


@dataclass(frozen=True, eq=True)
class Node:
    x: int
    y: int
    last_direction: int
    last_direction_count: int

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]
opposite_direction = {
    0: 1,
    1: 0,
    2: 3,
    3: 2,
}


def get_neighbours(node, grid):
    neighbours = []
    for did, (dx, dy) in enumerate(directions):
        if did == opposite_direction.get(node.last_direction):
            continue
        if node.last_direction_count == 3 and node.last_direction == did:
            continue
        nx, ny = node.x + dx, node.y + dy
        if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
            continue

        next_node = Node(nx, ny, did, node.last_direction_count + 1 if node.last_direction == did else 1)
        neighbours.append(next_node)
    return neighbours



def part1(text):
    grid = text.splitlines()
    pq = PriorityQueue()
    pq.put((0, Node(0, 0, -1, 0)))
    minimal_heat_loss = {}
    while not pq.empty():
        current_heat_loss, node = pq.get()
        for next_node in get_neighbours(node, grid):
            if next_node not in minimal_heat_loss:
                minimal_heat_loss[next_node] = current_heat_loss + int(grid[next_node.x][next_node.y])
                pq.put((minimal_heat_loss[next_node], next_node))

    return min(
        heat_loss
        for node, heat_loss in minimal_heat_loss.items()
        if node.x == len(grid) - 1 and node.y == len(grid[0]) - 1
    )
    


def part2(text):
    pass
