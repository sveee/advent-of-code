use phf::phf_map;
use std::collections::HashSet;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn add(self, other: Self) -> Self {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

const BOX: char = 'O';
const LEFT_BOX: char = '[';
const RIGHT_BOX: char = ']';
const ROBOT: char = '@';
const SPACE: char = '.';
const WALL: char = '#';

const LEFT: Point = Point { x: 0, y: -1 };
const RIGHT: Point = Point { x: 0, y: 1 };
const UP: Point = Point { x: -1, y: 0 };
const DOWN: Point = Point { x: 1, y: 0 };
const DIRECTIONS: phf::Map<char, Point> = phf_map! {
    '<' => LEFT,
    '>' => RIGHT,
    '^' => UP,
    'v' => DOWN,
};

fn within_bounds(p: Point, grid: &Vec<Vec<char>>) -> bool {
    p.x >= 0 && p.x < grid.len() as i32 && p.y >= 0 && p.y < grid[0].len() as i32
}

fn gps_coords(grid: &Vec<Vec<char>>) -> i32 {
    let mut total = 0;
    for x in 0..grid.len() {
        for y in 0..grid[0].len() {
            if grid[x][y] == BOX || grid[x][y] == LEFT_BOX {
                total += 100 * x as i32 + y as i32;
            }
        }
    }
    total
}

fn find_push_group(r: Point, d: Point, grid: &Vec<Vec<char>>) -> HashSet<Point> {
    if !within_bounds(r, grid) {
        return HashSet::new();
    }

    let mut stack = vec![r];
    let mut group = HashSet::new();

    while let Some(p) = stack.pop() {
        if !group.contains(&p)
            && grid[p.x as usize][p.y as usize] != WALL
            && grid[p.x as usize][p.y as usize] != SPACE
        {
            group.insert(p);

            if matches!(
                grid[p.x as usize][p.y as usize],
                ROBOT | BOX | LEFT_BOX | RIGHT_BOX
            ) || (grid[p.x as usize][p.y as usize] == LEFT_BOX && d.x != 0)
            {
                let next_p = p.add(d);
                if !group.contains(&next_p) {
                    stack.push(next_p);
                }
            }

            if grid[p.x as usize][p.y as usize] == LEFT_BOX && d.x != 0 {
                let right_p = p.add(RIGHT);
                if !group.contains(&right_p) {
                    stack.push(right_p);
                }
            } else if grid[p.x as usize][p.y as usize] == RIGHT_BOX && d.x != 0 {
                let left_p = p.add(LEFT);
                if !group.contains(&left_p) {
                    stack.push(left_p);
                }
            }
        }
    }

    group
}

fn do_move(d: Point, grid: &mut Vec<Vec<char>>) {
    let robot_position = grid.iter().enumerate().find_map(|(x, row)| {
        row.iter().position(|&cell| cell == ROBOT).map(|y| Point {
            x: x as i32,
            y: y as i32,
        })
    });

    if let Some(r) = robot_position {
        let group = find_push_group(r, d, grid);
        let pushed_group: Vec<(Point, char)> = group
            .iter()
            .map(|&p| (p.add(d), grid[p.x as usize][p.y as usize]))
            .collect();

        if pushed_group
            .iter()
            .all(|&(p, _)| within_bounds(p, grid) && grid[p.x as usize][p.y as usize] != WALL)
        {
            for &p in &group {
                grid[p.x as usize][p.y as usize] = SPACE;
            }

            for &(p, v) in &pushed_group {
                grid[p.x as usize][p.y as usize] = v;
            }
        }
    }
}

fn simulate_moves(grid: &mut Vec<Vec<char>>, moves: &str) {
    for mv in moves.chars() {
        if let Some(&direction) = DIRECTIONS.get(&mv) {
            do_move(direction, grid);
        }
    }
}

fn parse_grid(text: &str) -> Vec<Vec<char>> {
    text.lines().map(|line| line.chars().collect()).collect()
}

fn part1(text: &str) -> i32 {
    let parts: Vec<&str> = text.split("\n\n").collect();
    let mut grid = parse_grid(parts[0]);
    simulate_moves(&mut grid, parts[1]);
    gps_coords(&grid)
}

fn part2(text: &str) -> i32 {
    let parts: Vec<&str> = text.split("\n\n").collect();
    let mut grid = parse_grid(
        &parts[0]
            .replace('#', "##")
            .replace('O', "[]")
            .replace('.', "..")
            .replace('@', "@."),
    );
    simulate_moves(&mut grid, parts[1]);
    gps_coords(&grid)
}

fn main() {
    aoc2024::solve(part1, part2);
}
