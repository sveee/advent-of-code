
import sys

allowed_direction = {
    '^': [(-1, 0)],
    'v': [(1, 0)],
    '<': [(0, -1)],
    '>': [(0, 1)],
    '.': [(-1, 0), (1, 0), (0, -1), (0, 1)],
}


def get_neighbours(posiiton, visited, grid):
    x, y = posiiton
    neighbours = []
    for dx, dy in allowed_direction[grid[x][y]]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != '#' and (nx, ny) not in visited:
            neighbours.append((nx, ny))
    return neighbours



def get_longest_hike(posiiton, f, visited, grid):
    x, y = posiiton
    if x == len(grid) - 1 and y == len(grid[0]) - 2:
        return 0

    if f[x][y] != -1:
        return f[x][y]
    longest_hike = -1
    for next_posiiton in get_neighbours(posiiton, visited, grid):
        visited.add(next_posiiton)
        longest_hike = max(longest_hike, get_longest_hike(next_posiiton, f, visited,grid) + 1)
        visited.remove(next_posiiton)
    f[x][y] =  longest_hike
    return longest_hike
    

def part1(text):
    grid = text.splitlines()
    f = [[-1 for _y in range(len(grid[1]))] for _x in range(len(grid))]
    return get_longest_hike((0, 1), f, set(), grid)



def part2(text):
    pass
