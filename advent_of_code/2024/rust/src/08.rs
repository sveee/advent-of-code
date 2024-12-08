use itertools::Itertools;
use std::collections::{HashMap, HashSet};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Point {
    x: i32,
    y: i32,
}

fn within_bounds(x: i32, y: i32, n: i32, m: i32) -> bool {
    x >= 0 && x < n && y >= 0 && y < m
}

fn get_antennas(grid: &[&str]) -> HashMap<char, Vec<Point>> {
    let mut antennas = HashMap::new();
    for (x, line) in grid.iter().enumerate() {
        for (y, ch) in line.chars().enumerate() {
            if ch != '.' {
                antennas.entry(ch).or_insert_with(Vec::new).push(Point {
                    x: x as i32,
                    y: y as i32,
                });
            }
        }
    }
    antennas
}

fn part1(text: &str) -> usize {
    let grid: Vec<&str> = text.lines().collect();
    let n = grid.len() as i32;
    let m = grid[0].len() as i32;

    let antennas = get_antennas(&grid);
    let mut locations = HashSet::new();

    for group in antennas.values() {
        for (a1, a2) in group.iter().tuple_combinations() {
            let an1 = Point {
                x: 2 * a1.x - a2.x,
                y: 2 * a1.y - a2.y,
            };
            let an2 = Point {
                x: 2 * a2.x - a1.x,
                y: 2 * a2.y - a1.y,
            };

            if within_bounds(an1.x, an1.y, n, m) {
                locations.insert(an1);
            }
            if within_bounds(an2.x, an2.y, n, m) {
                locations.insert(an2);
            }
        }
    }

    locations.len()
}

fn part2(text: &str) -> usize {
    let grid: Vec<&str> = text.lines().collect();
    let n = grid.len() as i32;
    let m = grid[0].len() as i32;

    let antennas = get_antennas(&grid);
    let mut locations = HashSet::new();

    for group in antennas.values() {
        for (a1, a2) in group.iter().tuple_combinations() {
            let d = Point {
                x: a2.x - a1.x,
                y: a2.y - a1.y,
            };

            let mut an = *a1;
            while within_bounds(an.x, an.y, n, m) {
                locations.insert(an);
                an = Point {
                    x: an.x - d.x,
                    y: an.y - d.y,
                };
            }

            an = *a2;
            while within_bounds(an.x, an.y, n, m) {
                locations.insert(an);
                an = Point {
                    x: an.x + d.x,
                    y: an.y + d.y,
                };
            }
        }
    }

    locations.len()
}

fn main() {
    aoc2024::solve(part1, part2);
}
