use regex::Regex;

#[derive(Debug, Clone, Copy)]
struct Point {
    x: i64,
    y: i64,
}

fn min_tokens(da: Point, db: Point, p: Point) -> i64 {
    let d = da.x * db.y - da.y * db.x;
    let mut a = p.x * db.y - p.y * db.x;
    let mut b = da.x * p.y - da.y * p.x;
    let mut d = d;

    if d < 0 {
        a = -a;
        b = -b;
        d = -d;
    }

    if a % d == 0 && b % d == 0 {
        return 3 * a / d + b / d;
    }

    0
}

fn get_machines(text: &str) -> Vec<(Point, Point, Point)> {
    let re = Regex::new(r"\d+").unwrap();

    text.split("\n\n")
        .filter_map(|machine| {
            let lines: Vec<&str> = machine.lines().collect();
            if lines.len() != 3 {
                return None;
            }

            let parse_point = |line: &str| -> Option<Point> {
                let mut numbers = re.find_iter(line).filter_map(|m| m.as_str().parse().ok());
                Some(Point {
                    x: numbers.next()?,
                    y: numbers.next()?,
                })
            };

            Some((
                parse_point(lines[0])?,
                parse_point(lines[1])?,
                parse_point(lines[2])?,
            ))
        })
        .collect()
}

fn part1(text: &str) -> i64 {
    get_machines(text)
        .into_iter()
        .map(|(da, db, p)| min_tokens(da, db, p))
        .sum()
}

const N: i64 = 10_000_000_000_000;

fn part2(text: &str) -> i64 {
    get_machines(text)
        .into_iter()
        .map(|(da, db, p)| {
            min_tokens(
                da,
                db,
                Point {
                    x: p.x + N,
                    y: p.y + N,
                },
            )
        })
        .sum()
}

fn main() {
    aoc2024::solve(part1, part2);
}
