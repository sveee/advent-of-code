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


def f(keypad, prev_button, current_button):
    paths = shortest_paths(keypad, prev_button, current_button)
    if keypad == 3:
        return len(paths[0]) + 1
    ans = 10**10
    for path in paths:
        for next_start, next_end in zip('A' + path, path):
            ans = min(ans, f(keypad + 1, next_start, next_end) + len(path))
    return ans


# def type_in(code, keypad):
#     if keypad == 3:
#         return [code]
#     seqs = ['']
#     for start, end in zip('A' + code, code):
#         seqs = [
#             prefix + suffix
#             for prefix in seqs
#             for path in shortest_paths(start, end, keypad)
#             for suffix in  type_in(path + 'A', keypad + 1)
#         ]
#         min_len = min(map(len, seqs))
#         seqs = [
#             seq
#             for seq in seqs
#             if len(seq) == min_len
#         ]
#     return seqs


def shortest_length(code, keypad):
    if keypad == 3:
        return len(code)

    ans = 0
    for start, end in zip('A' + code, code):
        ans += min(
            shortest_length(path + 'A', keypad + 1)
            for path in shortest_paths(start, end, keypad)
        )
    return ans


def part1(text):
    tests1()
    return sum(shortest_length(code, 0) * int(code[:-1]) for code in text.splitlines())


def part2(text):
    pass


def tests1():
    assert shortest_paths('A', '0', 0) == ['<']
    assert shortest_paths('0', '8', 0) == ['^^^']
    assert shortest_paths('8', '0', 0) == ['vvv']
    assert shortest_paths('2', '4', 0) == ['<^', '^<']

    # assert '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A' in type_in('029A', 0)
    assert shortest_length('029A', 0) == 68
    assert shortest_length('980A', 0) == 60
    assert shortest_length('179A', 0) == 68
    assert shortest_length('456A', 0) == 64
    assert shortest_length('379A', 0) == 64

    # assert False
    #  assert shortest_length('<A', 2) == len('v<<A>>^A')
    #  assert shortest_length('<', 1) == len('<vA<AA>>^A')
    #  assert shortest_length('<A', 1) == len('<vA<AA>>^AvAA<^A>A')
