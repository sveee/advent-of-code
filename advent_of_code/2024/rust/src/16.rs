use phf::phf_map;
use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::collections::{HashMap, HashSet, VecDeque};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct State {
    position: Point,
    direction: Point,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.position
            .x
            .cmp(&other.position.x)
            .then(self.position.y.cmp(&other.position.y))
            .then(self.direction.x.cmp(&other.direction.x))
            .then(self.direction.y.cmp(&other.direction.y))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

static DIRECTIONS: phf::Map<&'static str, Point> = phf_map! {
    "UP" => Point { x: -1, y: 0 },
    "DOWN" => Point { x: 1, y: 0 },
    "LEFT" => Point { x: 0, y: -1 },
    "RIGHT" => Point { x: 0, y: 1 },
};

fn find_value(grid: &[Vec<char>], value: char) -> Point {
    for (x, row) in grid.iter().enumerate() {
        for (y, &cell) in row.iter().enumerate() {
            if cell == value {
                return Point {
                    x: x as i32,
                    y: y as i32,
                };
            }
        }
    }
    panic!("Value not found in grid");
}

fn dijkstra(start: Point, grid: &[Vec<char>]) -> (HashMap<State, i32>, HashMap<State, Vec<State>>) {
    let start_state = State {
        position: start,
        direction: DIRECTIONS["RIGHT"],
    };

    let mut queue = BinaryHeap::new();
    let mut distance: HashMap<State, i32> = HashMap::new();
    let mut prev: HashMap<State, Vec<State>> = HashMap::new();

    distance.insert(start_state, 0);
    queue.push(Reverse((0, start_state)));

    while let Some(Reverse((priority, state))) = queue.pop() {
        for &direction in DIRECTIONS.values() {
            let next_state = State {
                position: state.position,
                direction,
            };

            if !distance.contains_key(&next_state) {
                distance.insert(next_state, priority + 1000);
                queue.push(Reverse((priority + 1000, next_state)));
            }
            if priority + 1000 == *distance.get(&next_state).unwrap() {
                prev.entry(next_state).or_default().push(state);
            }
        }

        let next_position = Point {
            x: state.position.x + state.direction.x,
            y: state.position.y + state.direction.y,
        };

        if grid[next_position.x as usize][next_position.y as usize] != '#' {
            let next_state = State {
                position: next_position,
                direction: state.direction,
            };

            if !distance.contains_key(&next_state) {
                distance.insert(next_state, priority + 1);
                queue.push(Reverse((priority + 1, next_state)));
            }
            if priority + 1 == *distance.get(&next_state).unwrap() {
                prev.entry(next_state).or_default().push(state);
            }
        }
    }

    (distance, prev)
}

fn parse_grid(input: &str) -> Vec<Vec<char>> {
    input.lines().map(|line| line.chars().collect()).collect()
}

fn part1(input: &str) -> i32 {
    let grid = parse_grid(input);
    let start = find_value(&grid, 'S');
    let end = find_value(&grid, 'E');

    let (distance, _) = dijkstra(start, &grid);

    DIRECTIONS
        .values()
        .map(|&direction| {
            let end_state = State {
                position: end,
                direction,
            };
            *distance.get(&end_state).unwrap_or(&i32::MAX)
        })
        .min()
        .unwrap()
}

fn part2(input: &str) -> i32 {
    let grid = parse_grid(input);
    let start = find_value(&grid, 'S');
    let end = find_value(&grid, 'E');

    let (distance, prev) = dijkstra(start, &grid);

    let best_end_state = DIRECTIONS
        .values()
        .map(|&direction| State {
            position: end,
            direction,
        })
        .min_by_key(|state| distance.get(state).unwrap_or(&i32::MAX))
        .unwrap();

    let mut paths = HashSet::new();
    let mut stack = VecDeque::new();

    paths.insert(best_end_state);
    stack.push_back(best_end_state);

    while let Some(state) = stack.pop_front() {
        if let Some(previous_states) = prev.get(&state) {
            for &prev_state in previous_states {
                if paths.insert(prev_state) {
                    stack.push_back(prev_state);
                }
            }
        }
    }

    paths
        .iter()
        .map(|state| state.position)
        .collect::<HashSet<_>>()
        .len() as i32
}

fn main() {
    aoc2024::solve(part1, part2);
}
