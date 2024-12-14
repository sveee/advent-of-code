use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::ops::Rem;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Clone, Copy, Debug)]
struct Robot {
    position: Point,
    velocity: Point,
}

impl Robot {
    fn move_robot(&self, size: &Point) -> Robot {
        let new_x = (self.position.x + self.velocity.x + size.x).rem(size.x);
        let new_y = (self.position.y + self.velocity.y + size.y).rem(size.y);
        Robot {
            position: Point { x: new_x, y: new_y },
            velocity: self.velocity,
        }
    }
}

const DIRECTIONS: [(i32, i32); 8] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
];
const W: i32 = 101;
const H: i32 = 103;

fn get_quadrant(p: &Point, v: &Point, s: &Point, k: i32) -> Option<i32> {
    let x = (p.x + k * (v.x + s.x)).rem(s.x);
    let y = (p.y + k * (v.y + s.y)).rem(s.y);
    let mx = s.x / 2;
    let my = s.y / 2;

    if x > mx && y < my {
        Some(1)
    } else if x < mx && y < my {
        Some(2)
    } else if x < mx && y > my {
        Some(3)
    } else if x > mx && y > my {
        Some(4)
    } else {
        None
    }
}

fn count_components(positions: &HashSet<Point>, size: &Point) -> i32 {
    let mut visited = HashSet::new();
    let mut n_components = 0;

    for &pos in positions {
        if !visited.contains(&pos) {
            let mut stack = vec![pos];
            visited.insert(pos);
            while let Some(p) = stack.pop() {
                for (dx, dy) in DIRECTIONS.iter() {
                    let np = Point {
                        x: p.x + dx,
                        y: p.y + dy,
                    };
                    if np.x >= 0 && np.x < size.x && np.y >= 0 && np.y < size.y {
                        if !visited.contains(&np) && positions.contains(&np) {
                            visited.insert(np);
                            stack.push(np);
                        }
                    }
                }
            }
            n_components += 1;
        }
    }

    n_components
}

fn part1(text: &str) -> i32 {
    let size = Point { x: W, y: H };
    let re = Regex::new(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)").unwrap();

    let mut n_per_quadrant: HashMap<i32, i32> = HashMap::new();
    for line in text.lines() {
        if let Some(cap) = re.captures(line) {
            let px: i32 = cap[1].parse().unwrap();
            let py: i32 = cap[2].parse().unwrap();
            let vx: i32 = cap[3].parse().unwrap();
            let vy: i32 = cap[4].parse().unwrap();

            let p = Point { x: px, y: py };
            let v = Point { x: vx, y: vy };
            if let Some(q) = get_quadrant(&p, &v, &size, 100) {
                *n_per_quadrant.entry(q).or_insert(0) += 1;
            }
        }
    }

    n_per_quadrant.values().fold(1, |a, &b| a * b)
}

fn part2(text: &str) -> i32 {
    let size = Point { x: W, y: H };
    let re = Regex::new(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)").unwrap();

    let mut robots: Vec<Robot> = text
        .lines()
        .filter_map(|line| {
            re.captures(line).map(|cap| {
                let px: i32 = cap[1].parse().unwrap();
                let py: i32 = cap[2].parse().unwrap();
                let vx: i32 = cap[3].parse().unwrap();
                let vy: i32 = cap[4].parse().unwrap();
                Robot {
                    position: Point { x: px, y: py },
                    velocity: Point { x: vx, y: vy },
                }
            })
        })
        .collect();

    let mut min_n_components = robots.len() as i32;
    let mut tree_seconds = 0;
    for seconds in 0..(W * H) {
        let positions: HashSet<Point> = robots.iter().map(|r| r.position).collect();
        let n_components = count_components(&positions, &size);
        if n_components < min_n_components {
            min_n_components = n_components;
            tree_seconds = seconds;
        }
        robots = robots.iter().map(|r| r.move_robot(&size)).collect();
    }

    tree_seconds
}

fn main() {
    aoc2024::solve(part1, part2);
}
