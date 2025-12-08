
from queue import PriorityQueue
from scipy.cluster.hierarchy import DisjointSet

def dist(p1, p2):
    return sum((a - b) ** 2 for a, b in zip(p1, p2))

def part1(text):
    points = [
        tuple(map(int, line.split(',')))
        for line in text.splitlines()
    ]
    queue = PriorityQueue()
    for index, point in enumerate(points):
        for other_index in range(index + 1, len(points)):
            queue.put((dist(point, points[other_index]), index, other_index))

    
    disjoint_set = DisjointSet(range(len(points)))
    n_connections = 0
    N = 10 if len(points) < 500 else 1000
    while n_connections < N:
        distance, index1, index2 = queue.get()
        if not disjoint_set.connected(index1, index2):
            disjoint_set.merge(index1, index2)
        n_connections += 1

    sizes = sorted(map(len, disjoint_set.subsets()), reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


def part2(text):
    points = [
        tuple(map(int, line.split(',')))
        for line in text.splitlines()
    ]
    queue = PriorityQueue()
    for index, point in enumerate(points):
        for other_index in range(index + 1, len(points)):
            queue.put((dist(point, points[other_index]), index, other_index))

    
    disjoint_set = DisjointSet(range(len(points)))
    last_index1, last_index2 = 0, 0
    while queue.qsize() > 0:
        distance, index1, index2 = queue.get()
        if not disjoint_set.connected(index1, index2):
            last_index1, last_index2 = index1, index2
            disjoint_set.merge(index1, index2)
    return points[last_index1][0] * points[last_index2][0]
