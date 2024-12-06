
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
    visited: &mut [bool],
    n: usize,
    m: usize,
) -> i32 {
    visited.fill(false);

    let (mut x, mut y) = (sx, sy);
    let mut mdi = di;
    let (n_i32, m_i32) = (n as i32, m as i32);

    while within_bounds(x, y, n_i32, m_i32) {
        let (dx, dy) = DIRECTIONS[mdi];

        let state_idx = if track_loop {
            (((x as usize) * m) + (y as usize)) * 4 + mdi
        } else {
            (x as usize) * m + (y as usize)
        };

        if visited[state_idx] && track_loop {
            return 1;
        }

        visited[state_idx] = true;

        let nx = x + dx;
        let ny = y + dy;

        if !within_bounds(nx, ny, n_i32, m_i32) {
            break;
        }

        if grid[nx as usize][ny as usize] == '#' {
            mdi = (mdi + 1) % 4;
        } else {
            x = nx;
            y = ny;
        }
    }

    if track_loop { 0 } else { visited.iter().filter(|&&v| v).count() as i32 }
}

fn part1(text: &str) -> i32 {
    let grid: Vec<Vec<char>> = text.lines().map(|line| line.chars().collect()).collect();
    let n = grid.len();
    let m = grid[0].len();

    let (sx, sy) = (0..n)
        .flat_map(|x| (0..m).map(move |y| (x, y)))
        .find(|&(x, y)| grid[x][y] == '^')
        .expect("No starting position found");

    let mut visited = vec![false; n*m];
    simulate_path(sx as i32, sy as i32, 0, &grid, false, &mut visited, n, m)
}

fn part2(text: &str) -> i32 {
    let mut grid: Vec<Vec<char>> = text.lines().map(|line| line.chars().collect()).collect();
    let n = grid.len();
    let m = grid[0].len();
    let (sx, sy) = (0..n)
        .flat_map(|x| (0..m).map(move |y| (x, y)))
        .find(|&(x, y)| grid[x][y] == '^')
        .expect("No starting position found");

    let mut visited = vec![false; n*m*4];
    let mut total = 0;
    for x in 0..n {
        for y in 0..m {
            if grid[x][y] == '.' {
                grid[x][y] = '#';
                total += simulate_path(sx as i32, sy as i32, 0, &grid, true, &mut visited, n, m);
                grid[x][y] = '.';
            }
        }
    }
    total
}

fn main() {
    aoc2024::solve(part1, part2);
}
