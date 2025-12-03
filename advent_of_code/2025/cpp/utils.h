#pragma once

#include <fstream>
#include <iostream>
#include <ranges>
#include <sstream>
#include <string>

const std::string read_file(const std::string &filename) {
    std::ifstream file_stream(filename);
    std::stringstream buffer;
    buffer << file_stream.rdbuf();
    return buffer.str();
}

const std::vector<std::string> split_lines(const std::string &input_data) {
    return input_data | std::views::split('\n') |
           std::views::transform([](auto &&rng) { return std::string(rng.begin(), rng.end()); }) |
           std::ranges::to<std::vector<std::string>>();
}

void solve(char *argv[], auto part_one_solver, auto part_two_solver) {
    std::string part_name = argv[1];
    std::string input_file = argv[2];

    const std::string input_data = read_file(input_file);
    std::string output;
    if (part_name == "part1") {
        output = part_one_solver(input_data);
    } else if (part_name == "part2") {
        output = part_two_solver(input_data);
    }
    std::cout << output << std::endl;
}