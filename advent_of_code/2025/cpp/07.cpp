
#include <iostream>
#include <set>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

#define N 150
#define EMPTY -1LL

long long mem[N][N];

void df(int x, int y, vector<string> &grid, set<pair<int, int>> &visited) {
    if (visited.contains({x, y})) {
        return;
    }

    visited.insert({x, y});
    if (grid[x][y] == '^') {
        if (y > 0) {
            df(x, y - 1, grid, visited);
        }
        if (y < grid.size() - 1) {
            df(x, y + 1, grid, visited);
        }
    } else if (x < grid[0].size() - 1) {
        df(x + 1, y, grid, visited);
    }
}

const string part1(const string &input) {
    vector<string> grid = split_string(input);
    set<pair<int, int>> visited;

    int sy = grid[0].find('S');

    df(0, sy, grid, visited);

    int total = 0;
    for (auto [vx, vy] : visited) {
        if (grid[vx][vy] == '^') {
            total++;
        }
    }
    return to_string(total);
}

long long dp(int x, int y, vector<string> &grid) {
    if (x == grid.size() - 1) {
        return 1LL;
    }

    if (mem[x][y] != EMPTY) {
        return mem[x][y];
    }

    long long total = 0LL;
    if (grid[x][y] == '^') {
        if (y > 0) {
            total += dp(x, y - 1, grid);
        }
        if (y < grid[0].size() - 1) {
            total += dp(x, y + 1, grid);
        }
    } else if (x < grid.size() - 1) {
        total += dp(x + 1, y, grid);
    }

    mem[x][y] = total;
    return total;
}

const string part2(const string &input) {
    vector<string> grid = split_string(input);
    set<pair<int, int>> visited;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            mem[i][j] = EMPTY;
        }
    }

    int sy = grid[0].find('S');
    long long total = dp(0, sy, grid);
    return to_string(total);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}