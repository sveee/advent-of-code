import re
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from typing import List, Optional


@dataclass(frozen=True)
class Segment:
    start: int
    end: int

    def intersect(self, other: 'Segment') -> Optional['Segment']:
        if self.end < other.start or other.end < self.start:
            return None
        return Segment(max(self.start, other.start), min(self.end, other.end))

    def contains(self, x):
        return self.start <= x <= self.end

    def size(self):
        return self.end - self.start + 1


MIN_VALUE = 1
MAX_VALUE = 4000


@dataclass
class Rule:
    letter: str
    next_name: str
    segment: Segment

    def negate(self) -> 'Rule':
        if self.segment.start == MIN_VALUE:
            assert self.segment.end + 1 <= MAX_VALUE
            return Rule(
                letter=self.letter,
                next_name=self.next_name,
                segment=Segment(self.segment.end + 1, MAX_VALUE),
            )
        else:
            assert MIN_VALUE <= self.segment.start - 1
            return Rule(
                letter=self.letter,
                next_name=self.next_name,
                segment=Segment(MIN_VALUE, self.segment.start - 1),
            )

    @staticmethod
    def from_str(s) -> 'Rule':
        letter, next_name, min_value, max_value = 'x', '', MIN_VALUE, MAX_VALUE
        if ':' in s:
            letter, sign, value, next_name = re.search(
                '^(\w+)([<>])(\d+):(\w+)', s
            ).groups()
            value = int(value)

            if sign == '<':
                max_value = value - 1
            else:
                min_value = value + 1
        else:
            next_name = s

        return Rule(
            letter=letter, next_name=next_name, segment=Segment(min_value, max_value)
        )


@dataclass
class Workflow:
    name: str
    rules: List[Rule]

    @staticmethod
    def from_str(s) -> 'Workflow':
        name, rules_str = re.search('^(\w+)\{(.+)\}$', s).groups()
        return Workflow(
            name, [Rule.from_str(rule_str) for rule_str in rules_str.split(',')]
        )


def is_accepted(xmas, workflow_by_name):
    name = 'in'
    while True:
        if name == 'A':
            return True
        elif name == 'R':
            return False

        for rule in workflow_by_name[name].rules:
            if rule.segment.contains(xmas[rule.letter]):
                name = rule.next_name
                break


def apply_rule(part_space, rule):
    if not part_space:
        return
    new_part_space = deepcopy(part_space)
    intersection = part_space[rule.letter].intersect(rule.segment)
    if not intersection:
        return
    new_part_space[rule.letter] = intersection
    return new_part_space


def find_acceptable_part_spaces(name, part_space, workflow_by_name):
    if name == 'A':
        return [part_space]
    elif name == 'R':
        return []

    rules = workflow_by_name[name].rules
    part_spaces = []
    for pos_index in range(len(rules)):
        current_part_space = deepcopy(part_space)
        for neg_index in range(pos_index):
            current_part_space = apply_rule(
                current_part_space, rules[neg_index].negate()
            )
        current_part_space = apply_rule(current_part_space, rules[pos_index])
        if not current_part_space:
            continue
        part_spaces.extend(
            find_acceptable_part_spaces(
                rules[pos_index].next_name, current_part_space, workflow_by_name
            )
        )
    return part_spaces


def part1(text):
    workflows_str, parts_str = text.split('\n\n')
    workflows = [Workflow.from_str(line) for line in workflows_str.splitlines()]
    workflow_by_name = {}
    for workflow in workflows:
        workflow_by_name[workflow.name] = workflow
    parts = [
        dict(zip('xmas', map(int, re.findall('\d+', line))))
        for line in parts_str.splitlines()
    ]
    total = 0
    for part in parts:
        if is_accepted(part, workflow_by_name):
            total += sum(part.values())
    return total


def part2(text):
    workflows_str, _parts_str = text.split('\n\n')
    workflows = [Workflow.from_str(line) for line in workflows_str.splitlines()]
    workflow_by_name = {}
    for workflow in workflows:
        workflow_by_name[workflow.name] = workflow
    initial_part_space = {
        letter: segment
        for letter, segment in zip(
            'xmas', [Segment(MIN_VALUE, MAX_VALUE) for _ in range(4)]
        )
    }
    part_spaces = find_acceptable_part_spaces(
        'in', initial_part_space, workflow_by_name
    )
    return sum(
        reduce(lambda x, y: x * y, [segment.size() for segment in part_space.values()])
        for part_space in part_spaces
    )
