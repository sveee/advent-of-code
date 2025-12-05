
#include <algorithm>
#include <cmath>
#include <iostream>
#include <ranges>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

int dx[8] = {-1, -1, -1, 0, 0, 1, 1, 1};
int dy[8] = {-1, 0, 1, -1, 1, -1, 0, 1};

const string part1(const string &input) {
    vector<string> lines = split_string(input);
    int n = lines.size();
    int m = lines[0].size();
    int total = 0;
    for (int x = 0; x < n; ++x) {
        for (int y = 0; y < m; ++y) {
            if (lines[x][y] != '@') {
                continue;
            }
            int n_rolls = 0;
            for (int k = 0; k < 8; ++k) {
                int nx = x + dx[k];
                int ny = y + dy[k];

                if (0 <= nx && nx < n && 0 <= ny && ny < m && lines[nx][ny] == '@') {
                    n_rolls++;
                }
            }
            if (n_rolls < 4) {
                total++;
            }
        }
    }

    return to_string(total);
}

const string part2(const string &input) {
    vector<vector<char>> grid =
        input | views::split('\n') |
        views::transform([](auto &&rng) { return vector<char>(rng.begin(), rng.end()); }) |
        ranges::to<vector<vector<char>>>();

    int removed = 0;
    while (true) {
        vector<vector<char>> new_grid = grid;
        bool changed = false;
        int n = grid.size();
        int m = grid[0].size();

        for (int x = 0; x < n; ++x) {
            for (int y = 0; y < m; ++y) {
                if (grid[x][y] != '@') {
                    continue;
                }
                int n_rolls = 0;
                for (int k = 0; k < 8; ++k) {
                    int nx = x + dx[k];
                    int ny = y + dy[k];

                    if (0 <= nx && nx < n && 0 <= ny && ny < m && grid[nx][ny] == '@') {
                        n_rolls++;
                    }
                }
                if (n_rolls < 4) {
                    new_grid[x][y] = '.';
                    removed++;
                    changed = true;
                }
            }
        }

        if (!changed) {
            break;
        }
        grid = new_grid;
    }
    return to_string(removed);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}