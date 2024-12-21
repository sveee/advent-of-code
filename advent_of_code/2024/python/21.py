from collections import deque

numeric_keypad = {
    'A': [('0', '<'), ('3', '^')],
    '0': [('2', '^'), ('A', '>')],
    '1': [('2', '>'), ('4', '^')],
    '2': [('0', 'v'), ('1', '<'), ('3', '>'), ('5', '^')],
    '3': [('A', 'v'), ('2', '<'), ('6', '^')],
    '4': [('1', 'v'), ('5', '>'), ('7', '^')],
    '5': [('2', 'v'), ('4', '<'), ('6', '>'), ('8', '^')],
    '6': [('3', 'v'), ('5', '<'), ('9', '^')],
    '7': [('4', 'v'), ('8', '>')],
    '8': [('5', 'v'), ('7', '<'), ('9', '>')],
    '9': [('6', 'v'), ('8', '<')],
}

directional_keypad = {
    '<': [('v', '>')],
    'v': [('<', '<'), ('^', '^'), ('>', '>')],
    '>': [('v', '<'), ('A', '^')],
    '^': [('v', 'v'), ('A', '>')],
    'A': [('^', '<'), ('>', 'v')],
}


def shortest_paths(start, end, keypad):
    graph = directional_keypad if keypad != 0 else numeric_keypad
    queue = deque([(start, '')])
    paths = []
    while len(queue) > 0:
        history, directions = queue.popleft()
        if history[-1] == end:
            if not paths or len(paths[-1]) == len(directions):
                paths.append(directions)
        if paths and len(history) > len(paths[0]) + 1:
            continue
        for next_node, direction in graph[history[-1]]:
            if next_node not in history:
                queue.append((history + next_node, directions + direction))
    return paths


def shortest_length(code, keypad, n, cache):
    if keypad == n:
        return len(code)

    state = code, keypad
    if state in cache:
        return cache[state]

    ans = 0
    for start, end in zip('A' + code, code):
        ans += min(
            shortest_length(path + 'A', keypad + 1, n, cache)
            for path in shortest_paths(start, end, keypad)
        )
    cache[state] = ans
    return ans


def part1(text):
    tests1()
    cache = {}
    return sum(
        shortest_length(code, 0, 3, cache) * int(code[:-1])
        for code in text.splitlines()
    )


def part2(text):
    cache = {}
    return sum(
        shortest_length(code, 0, 26, cache) * int(code[:-1])
        for code in text.splitlines()
    )


def tests1():
    assert shortest_paths('A', '0', 0) == ['<']
    assert shortest_paths('0', '8', 0) == ['^^^']
    assert shortest_paths('8', '0', 0) == ['vvv']
    assert shortest_paths('2', '4', 0) == ['<^', '^<']

    assert shortest_length('029A', 0, 3, {}) == 68
    assert shortest_length('980A', 0, 3, {}) == 60
    assert shortest_length('179A', 0, 3, {}) == 68
    assert shortest_length('456A', 0, 3, {}) == 64
    assert shortest_length('379A', 0, 3, {}) == 64
