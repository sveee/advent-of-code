
from datetime import datetime
import yaml
import os


# problem_template = '''
# from aoc.problem import Problem


# class Promblem{year}_{day}(Problem):
#     def part1(self, text):
#         return None

#     def part2(self, text):
#         return None


# Promblem{year}_{day}().check_test()
# Promblem{year}_{day}().submit()
# '''


def main():
    # now = datetime.now()
    print(os.listdir())
    with open('aoc/2023/tests/10.yml', 'w') as f:
        yaml.dump(
            dict(part1=[{'input': '''12
34''', 'output': '2'}])
        )
        
if __name__ == '__main__':
    main()