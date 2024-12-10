use std::collections::HashSet;

static DIRECTIONS: &[(isize, isize)] = &[(-1, 0), (1, 0), (0, -1), (0, 1)];

fn within_bounds(x: isize, y: isize, grid: &[&str]) -> bool {
    let n = grid.len();
    let m = grid[0].len();
    x >= 0 && y >= 0 && (x as usize) < n && (y as usize) < m
}

fn trailhead_score(x: usize, y: usize, grid: &[&str]) -> HashSet<(usize, usize)> {
    let current = grid[x].as_bytes()[y];
    let mut total = HashSet::new();
    if current == b'9' {
        total.insert((x, y));
        return total;
    }
    for &(dx, dy) in DIRECTIONS.iter() {
        let nx = x as isize + dx;
        let ny = y as isize + dy;
        if within_bounds(nx, ny, grid) {
            let (nxu, nyu) = (nx as usize, ny as usize);
            let next_val = grid[nxu].as_bytes()[nyu];
            if next_val as i32 - current as i32 == 1 {
                total.extend(trailhead_score(nxu, nyu, grid));
            }
        }
    }
    total
}

fn trailhead_score2(x: usize, y: usize, grid: &[&str]) -> usize {
    let current = grid[x].as_bytes()[y];
    if current == b'9' {
        return 1;
    }

    let mut total = 0;
    for &(dx, dy) in DIRECTIONS.iter() {
        let nx = x as isize + dx;
        let ny = y as isize + dy;
        if within_bounds(nx, ny, grid) {
            let (nxu, nyu) = (nx as usize, ny as usize);
            let next_val = grid[nxu].as_bytes()[nyu];
            if next_val as i32 - current as i32 == 1 {
                total += trailhead_score2(nxu, nyu, grid);
            }
        }
    }
    total
}

fn part1(text: &str) -> usize {
    let grid: Vec<&str> = text.lines().collect();
    let mut sum = 0;
    for x in 0..grid.len() {
        for y in 0..grid[0].len() {
            if grid[x].as_bytes()[y] == b'0' {
                sum += trailhead_score(x, y, &grid).len();
            }
        }
    }
    sum
}

fn part2(text: &str) -> usize {
    let grid: Vec<&str> = text.lines().collect();
    let mut sum = 0;
    for x in 0..grid.len() {
        for y in 0..grid[0].len() {
            if grid[x].as_bytes()[y] == b'0' {
                sum += trailhead_score2(x, y, &grid);
            }
        }
    }
    sum
}

fn main() {
    aoc2024::solve(part1, part2);
}
