// src/lib.rs

use std::fs;
use std::process;

pub fn solve<F1, F2, R>(part1: F1, part2: F2)
where
    F1: Fn(&str) -> R,
    F2: Fn(&str) -> R,
    R: ToString,
{
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 3 {
        eprintln!("Usage: {} <part1|part2> <input_file>", args[0]);
        process::exit(1);
    }

    let part = &args[1];
    let input_file = &args[2];
    let input = fs::read_to_string(input_file).expect("Failed to read input file");

    match part.as_str() {
        "part1" => println!("{}", part1(&input).to_string()),
        "part2" => println!("{}", part2(&input).to_string()),
        _ => {
            eprintln!("Invalid part: {}", part);
            process::exit(1);
        }
    }
}
