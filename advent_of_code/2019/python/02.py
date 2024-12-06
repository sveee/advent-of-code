def run_program(memory, noun, verb):
    memory = memory.copy()
    memory[1] = noun
    memory[2] = verb
    index = 0
    while index < len(memory):
        value = memory[index]
        if value == 1:
            memory[memory[index + 3]] = (
                memory[memory[index + 1]] + memory[memory[index + 2]]
            )
            index += 4
        elif value == 2:
            memory[memory[index + 3]] = (
                memory[memory[index + 1]] * memory[memory[index + 2]]
            )
            index += 4
        elif value == 99:
            break
        else:
            index += 1
    return memory[0]


def part1(text, test=False):
    memory = list(map(int, text.split(',')))
    if not test:
        noun, verb = 12, 2
    else:
        noun, verb = memory[1], memory[2]
    return run_program(memory, noun, verb)


def part2(text):
    memory = list(map(int, text.split(',')))
    return next(
        100 * noun + verb
        for noun in range(100)
        for verb in range(100)
        if run_program(memory, noun, verb) == 19690720
    )
