from collections import defaultdict, deque


def part1(text):
    graph = defaultdict(list)
    for line in text.splitlines():
        left, right = line.split(')')
        graph[left].append(right)
    n_orbits, queue = {}, deque(['COM'])
    n_orbits['COM'] = 0
    while len(queue) > 0:
        node = queue.popleft()
        for next_node in graph[node]:
            if next_node in n_orbits:
                continue
            n_orbits[next_node] = n_orbits[node] + 1
            queue.append(next_node)
    return sum(n_orbits.values())


def part2(text):
    pass
