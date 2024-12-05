from collections import defaultdict


def order_pages(pages, rules):
    in_degree = {page: 0 for page in pages}
    for left in pages:
        for right in rules[left]:
            if right in in_degree:
                in_degree[right] += 1
    zero_in_degree = [node for node in in_degree if in_degree[node] == 0]
    ordered_pages = []
    while zero_in_degree:
        page = zero_in_degree.pop()
        ordered_pages.append(page)
        for right in rules[page]:
            if right not in in_degree:
                continue
            in_degree[right] -= 1
            if in_degree[right] == 0:
                zero_in_degree.append(right)
    return ordered_pages


def middle_page_number_sum(text, only_ordered):
    ordering_rules, pages_in_update = text.split('\n\n')
    rules = defaultdict(list)
    for line in ordering_rules.splitlines():
        left, right = line.split('|')
        rules[left].append(right)

    total = 0
    for line in pages_in_update.splitlines():
        pages = line.split(',')
        ordered_pages = order_pages(pages, rules)
        take = pages == ordered_pages if only_ordered else pages != ordered_pages
        if take:
            total += int(ordered_pages[len(pages) // 2])
    return total


def part1(text):
    return middle_page_number_sum(text, True)


def part2(text):
    return middle_page_number_sum(text, False)
