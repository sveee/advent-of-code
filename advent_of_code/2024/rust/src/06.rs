use std::collections::HashSet;

static DIRECTIONS: [(i32, i32); 4] = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1),
];

fn within_bounds(x: i32, y: i32, n: i32, m: i32) -> bool {
    x >= 0 && x < n && y >= 0 && y < m
}

fn simulate_path(
    sx: i32,
    sy: i32,
    di: usize,
    grid: &[Vec<char>],
    track_loop: bool,
) -> i32 {
    let n = grid.len() as i32;
    let m = grid[0].len() as i32;

    let mut visited_states = HashSet::new();
    let (mut x, mut y) = (sx, sy);
    let mut mdi = di;

    while within_bounds(x, y, n, m) {
        let (dx, dy) = DIRECTIONS[mdi];

        if track_loop {
            let state = (x, y, dx, dy);
            if visited_states.contains(&state) {
                return 1;
            }
            visited_states.insert(state);
        } else {
            let state = (x, y, 0, 0);
            visited_states.insert(state);
        }

        let nx = x + dx;
        let ny = y + dy;
        if !within_bounds(nx, ny, n, m) {
            break;
        }

        if grid[nx as usize][ny as usize] == '#' {
            mdi = (mdi + 1) % 4;
        } else {
            x = nx;
            y = ny;
        }
    }

    if track_loop {
        0
    } else {
        visited_states.len() as i32
    }
}

fn part1(text: &str) -> i32 {
    let grid: Vec<Vec<char>> = text.lines().map(|line| line.chars().collect()).collect();
    let n = grid.len();
    let m = grid[0].len();
    let (sx, sy) = (0..n)
        .flat_map(|x| (0..m).map(move |y| (x, y)))
        .find(|&(x, y)| grid[x][y] == '^')
        .expect("No starting position found");

    simulate_path(sx as i32, sy as i32, 0, &grid, false)
}

fn part2(text: &str) -> i32 {
    let mut grid: Vec<Vec<char>> = text.lines().map(|line| line.chars().collect()).collect();
    let n = grid.len();
    let m = grid[0].len();
    let (sx, sy) = (0..n)
        .flat_map(|x| (0..m).map(move |y| (x, y)))
        .find(|&(x, y)| grid[x][y] == '^')
        .expect("No starting position found");

    let mut total = 0;
    for x in 0..n {
        for y in 0..m {
            if grid[x][y] == '.' {
                grid[x][y] = '#';
                total += simulate_path(sx as i32, sy as i32, 0, &grid, true);
                grid[x][y] = '.';
            }
        }
    }
    total
}

fn main() {
    aoc2024::solve(part1, part2);
}
