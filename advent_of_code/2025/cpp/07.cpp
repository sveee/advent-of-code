
#include <iostream>
#include <string>
#include <vector>
#include <unordered_set>
#include <set>

#include "utils.h"

using namespace std;


// struct pair_hash {
//     size_t operator () (const pair<int, int> &p) const {
//         size_t h1 = hash<int>{}(p.first);
//         size_t h2 = hash<int>{}(p.second);
//         return h1 ^ (h2 << 1); 
//     }
// };


void df(int x, int y, vector<string> &grid, set<pair<int, int>> &visited) {
    
    // cout << x << "," << y << "\n";

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
    } else if(x < grid[0].size() - 1) {
        df(x + 1, y, grid, visited);
    }
}

const string part1(const string &input) {
    vector<string> grid = split_string(input);
    set<pair<int, int>> visited;

    int x = 0;
    int y = grid[0].find('S');

    df(x, y, grid, visited);

    int total = 0;
    for (auto [vx, vy] : visited) {
        if (grid[vx][vy] == '^') {
            total++;
        }
    }
    return to_string(total);
}

const string part2(const string &input) {
    vector<string> lines = split_string(input);

    return "";
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}