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


def get_path(node, prev):
    print(node, prev)
    path = []
    while node != 'COM':
        path.append(node)
        node = prev[node]
    return path[::-1]


def part2(text):
    prev = {}
    for line in text.splitlines():
        left, right = line.split(')')
        prev[right] = left
    path1 = get_path('YOU', prev)
    path2 = get_path('SAN', prev)
    index = 0
    while path1[index] == path2[index]:
        index += 1
    return len(path1) + len(path2) - 2 * index - 2
