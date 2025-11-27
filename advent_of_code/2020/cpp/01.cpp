
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

const string part1(const string &input) {
    vector<int> lines =
        input | views::split('\n') |
        views::transform([](auto &&rng) { return stoi(string(rng.begin(), rng.end())); }) |
        ranges::to<vector<int>>();
    int n = lines.size();
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (lines[i] + lines[j] == 2020) {
                return to_string(lines[i] * lines[j]);
            }
        }
    }
    return "";
}

const string part2(const string &input) {
    vector<int> lines =
        input | views::split('\n') |
        views::transform([](auto &&rng) { return stoi(string(rng.begin(), rng.end())); }) |
        ranges::to<vector<int>>();
    int n = lines.size();
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            for (int k = j + 1; k < n; ++k) {
                if (lines[i] + lines[j] + lines[k] == 2020) {
                    return to_string((long long)lines[i] * lines[j] * lines[k]);
                }
            }
        }
    }
    return "";
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}