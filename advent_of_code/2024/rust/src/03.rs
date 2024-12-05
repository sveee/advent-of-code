use regex::Regex;

fn part1(text: &str) -> i32 {
    let re = Regex::new(r"mul\(\d+,\d+\)").unwrap();
    let digit_re = Regex::new(r"\d+").unwrap();
    let mut total = 0;

    for expr in re.find_iter(text) {
        let numbers: Vec<i32> = digit_re
            .find_iter(expr.as_str())
            .map(|num| num.as_str().parse::<i32>().unwrap())
            .collect();
        if let [left, right] = numbers.as_slice() {
            total += left * right;
        }
    }

    total
}

fn part2(text: &str) -> i32 {
    let re = Regex::new(r"mul\(\d+,\d+\)|do\(\)|don't\(\)").unwrap();
    let digit_re = Regex::new(r"\d+").unwrap();
    let mut total = 0;
    let mut enabled = true;

    for expr in re.find_iter(text) {
        match expr.as_str() {
            "do()" => enabled = true,
            "don't()" => enabled = false,
            _ => {
                if enabled {
                    let numbers: Vec<i32> = digit_re
                        .find_iter(expr.as_str())
                        .map(|num| num.as_str().parse::<i32>().unwrap())
                        .collect();
                    if let [left, right] = numbers.as_slice() {
                        total += left * right;
                    }
                }
            }
        }
    }

    total
}

fn main() {
    aoc2024::solve(part1, part2);
}
