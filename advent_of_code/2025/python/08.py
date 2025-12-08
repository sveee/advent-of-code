from queue import PriorityQueue
from scipy.cluster.hierarchy import DisjointSet


def dist(p1, p2):
    return sum((a - b) ** 2 for a, b in zip(p1, p2))


def create_queue(points):
    queue = PriorityQueue()
    n = len(points)
    for index1 in range(n):
        for index2 in range(index1 + 1, n):
            queue.put((dist(points[index1], points[index2]), index1, index2))
    return queue


def part1(text):
    points = [tuple(map(int, line.split(','))) for line in text.splitlines()]
    queue = create_queue(points)
    disjoint_set = DisjointSet(range(len(points)))
    N = 10 if len(points) < 500 else 1000
    for _ in range(N):
        _, index1, index2 = queue.get()
        if not disjoint_set.connected(index1, index2):
            disjoint_set.merge(index1, index2)
    sizes = sorted(map(len, disjoint_set.subsets()), reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


def part2(text):
    points = [tuple(map(int, line.split(','))) for line in text.splitlines()]
    queue = create_queue(points)
    disjoint_set = DisjointSet(range(len(points)))
    last_index1, last_index2 = 0, 0
    while queue.qsize() > 0:
        _, index1, index2 = queue.get()
        if not disjoint_set.connected(index1, index2):
            last_index1, last_index2 = index1, index2
            disjoint_set.merge(index1, index2)
    return points[last_index1][0] * points[last_index2][0]
