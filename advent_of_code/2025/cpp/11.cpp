
#include <algorithm>
#include <cmath>
#include <iostream>
#include <map>
#include <ranges>
#include <set>
#include <sstream>
#include <stack>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;
typedef long long ll;
typedef map<string, vector<string>> Graph;

ll dfs(const string &start, const string &end, Graph &graph, map<string, ll> &memo) {
    if (memo.contains(start)) {
        return memo[start];
    }
    if (start == end) {
        return 1;
    }
    if (!graph.contains(start) || graph[start].empty()) {
        return 0;
    }
    ll total = 0;
    for (const string &neighbor : graph[start]) {
        total += dfs(neighbor, end, graph, memo);
    }
    memo[start] = total;
    return total;
}

Graph read_graph(const string &input) {
    vector<string> lines = split_string(input);
    Graph graph;
    for (const string &line : lines) {
        vector<string> parts = split_string(line, " ");
        string start = parts[0].substr(0, parts[0].size() - 1);
        for (int i = 1; i < parts.size(); ++i) {
            graph[start].push_back(parts[i]);
        }
    }
    return graph;
}

const string part1(const string &input) {
    Graph graph = read_graph(input);
    map<string, ll> memo;
    return to_string(dfs("you", "out", graph, memo));
}

const string part2(const string &input) {
    Graph graph = read_graph(input);

    ll total = 1;
    map<string, ll> memo;
    total *= dfs("svr", "fft", graph, memo);
    memo.clear();
    total *= dfs("fft", "dac", graph, memo);
    memo.clear();
    total *= dfs("dac", "out", graph, memo);

    return to_string(total);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}