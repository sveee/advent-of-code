
from dataclasses import dataclass
import re
from typing import List

@dataclass
class Rule:
    letter: str
    next_name: str
    min_value: int = -1
    max_value: int = 10**10

    @staticmethod
    def from_str(s) -> 'Rule':

        if ':' in s:
            letter, sign, value, next_name = re.search('^(\w+)([<>])(\d+):(\w+)', s).groups()
            value = int(value)
        else:
            letter, sign, value, next_name = 'x', '>', -1, s
        params = dict(
            letter=letter,
            next_name=next_name,
        )
        if sign == '<':
            params['max_value'] = value
        else:
            params['min_value'] = value


        return Rule(
            **params,
        )


@dataclass
class Workflow:
    name: str
    rules: List[Rule]

    @staticmethod
    def from_str(s) -> 'Workflow':
        name, rules_str = re.search('^(\w+)\{(.+)\}$', s).groups()
        return Workflow(
            name,
            [Rule.from_str(rule_str) for rule_str in rules_str.split(',')]
        )


def is_accepted(xmas, workflow_by_name):
    name = 'in'
    while True:
        if name == 'A':
            return True
        elif name == 'R':
            return False

        for rule in workflow_by_name[name].rules:
            if rule.min_value < xmas[rule.letter] < rule.max_value:
                name = rule.next_name
                break


def part1(text):
    workflows_str, parts_str = text.split('\n\n')
    workflows = [
        Workflow.from_str(line)
        for line in workflows_str.splitlines()
    ]
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
    pass
