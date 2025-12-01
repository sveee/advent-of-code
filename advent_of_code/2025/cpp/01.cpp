
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

const string part1(const string &input) {
    vector<string> lines =
        input | views::split('\n') |
        views::transform([](auto &&rng) { return string(rng.begin(), rng.end()); }) |
        ranges::to<vector<string>>();
    int dial = 50;
    int password = 0;
    for (auto &line : lines) {
        int direction = (line[0] == 'L') ? -1 : 1;
        int value = stoi(line.substr(1));
        dial = (dial + direction * value + 100) % 100;
        if (dial == 0) {
            ++password;
        }
    }
    return to_string(password);
}

const string part2(const string &input) {
    return "";
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}