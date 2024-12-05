fn get_fuel(mass: i32) -> i32 {
    (mass / 3) as i32 - 2
}

fn get_total_fuel(mass: i32) -> i32 {
    let mut total = 0;
    let mut fuel = get_fuel(mass);
    while fuel > 0 {
        total += fuel;
        fuel = get_fuel(fuel);
    }
    total
}

fn part1(input: &str) -> i32 {
    input
        .lines()
        .map(|x| get_fuel(x.parse::<i32>().unwrap()))
        .sum()
}

fn part2(input: &str) -> i32 {
    input
        .lines()
        .map(|x| get_total_fuel(x.parse::<i32>().unwrap()))
        .sum()
}

fn main() {
    aoc2019::solve(part1, part2);
}
