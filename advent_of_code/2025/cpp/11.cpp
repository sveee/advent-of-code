
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

ll dfs(const string &node, Graph &graph, map<string, ll> &memo) {
    if (memo.contains(node)) {
        return memo[node];
    }
    if (!graph.contains(node) || graph[node].empty()) {
        return 1;
    }
    ll total = 0;
    for (const string &neighbor : graph[node]) {
        total += dfs(neighbor, graph, memo);
    }
    memo[node] = total;
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
    return to_string(dfs("you", graph, memo));
}

Graph reverse_graph(const Graph &graph) {
    Graph reversed;
    for (const auto &[node, neighbors] : graph) {
        for (const string &neighbor : neighbors) {
            reversed[neighbor].push_back(node);
        }
    }
    return reversed;
}

Graph get_subgraph(const string &end, const Graph &graph) {
    Graph reversed = reverse_graph(graph);
    set<string> subgraph_nodes{end};
    stack<string> stack;
    stack.push(end);
    while (!stack.empty()) {
        string node = stack.top();
        stack.pop();
        if (!reversed.contains(node)) {
            continue;
        }
        for (const string &neighbor : reversed.at(node)) {
            if (!subgraph_nodes.contains(neighbor)) {
                subgraph_nodes.insert(neighbor);
                stack.push(neighbor);
            }
        }
    }

    Graph subgraph;
    for (const string &node : subgraph_nodes) {
        if (graph.contains(node)) {
            for (const string &neighbor : graph.at(node)) {
                if (subgraph_nodes.contains(neighbor)) {
                    subgraph[node].push_back(neighbor);
                }
            }
        }
    }
    return subgraph;
}

ll n_paths_between(const string &start, const string &end, const Graph &graph) {
    Graph subgraph = get_subgraph(end, graph);
    map<string, ll> memo;
    return dfs(start, subgraph, memo);
}

const string part2(const string &input) {
    Graph graph = read_graph(input);
    ll total = n_paths_between("svr", "fft", graph) * n_paths_between("fft", "dac", graph) *
               n_paths_between("dac", "out", graph);

    return to_string(total);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}