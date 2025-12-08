
#include <algorithm>
#include <cmath>
#include <functional>
#include <iostream>
#include <map>
#include <queue>
#include <ranges>
#include <sstream>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

struct Point {
    long long x;
    long long y;
    long long z;
};

struct DistancePair {
    long long dist;
    int index1;
    int index2;
};

struct CompareDistancePair {
    bool operator()(const DistancePair& a, const DistancePair& b) {
        return a.dist > b.dist;
    }
};

int find(int x, vector<int>& parent) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

void union_sets(int x, int y, vector<int>& parent) {
    x = find(x, parent);
    y = find(y, parent);
    if (x == y) {
        return;
    }
    parent[y] = x;
}

vector<Point> create_points(const string& input) {
    vector<string> lines = split_string(input);
    vector<Point> points;
    long long x, y, z;
    char comma1, comma2;
    for (const string& line : lines) {
        stringstream ss(line);
        ss >> x >> comma1 >> y >> comma2 >> z;
        points.push_back(Point{x, y, z});
    }
    return points;
}

auto create_min_heap(vector<Point>& points) {
    priority_queue<DistancePair, vector<DistancePair>, CompareDistancePair> min_heap;
    for (int i = 0; i < points.size(); ++i) {
        for (int j = i + 1; j < points.size(); ++j) {
            long long dist = (points[i].x - points[j].x) * (points[i].x - points[j].x) +
                             (points[i].y - points[j].y) * (points[i].y - points[j].y) +
                             (points[i].z - points[j].z) * (points[i].z - points[j].z);
            min_heap.push(DistancePair{dist, i, j});
        }
    }
    return min_heap;
}

const string part1(const string& input) {
    vector<Point> points = create_points(input);
    auto min_heap = create_min_heap(points);
    int N = points.size() < 500 ? 10 : 1000;
    vector<int> parent(points.size());
    for (int x = 0; x < points.size(); ++x) {
        parent[x] = x;
    }
    for (int i = 0; i < N; ++i) {
        DistancePair dist_pair = min_heap.top();
        min_heap.pop();
        if (find(dist_pair.index1, parent) != find(dist_pair.index2, parent)) {
            union_sets(dist_pair.index1, dist_pair.index2, parent);
        }
    }
    map<int, int> clusters_sizes_by_root;
    for (int x = 0; x < points.size(); ++x) {
        int root = find(x, parent);
        clusters_sizes_by_root[root]++;
    }
    vector<int> clusters_sizes;
    for (const auto& [root, size] : clusters_sizes_by_root) {
        clusters_sizes.push_back(size);
    }
    sort(clusters_sizes.begin(), clusters_sizes.end(), greater<int>());
    return to_string((long long)clusters_sizes[0] * clusters_sizes[1] * clusters_sizes[2]);
}

const string part2(const string& input) {
    vector<Point> points = create_points(input);
    auto min_heap = create_min_heap(points);
    vector<int> parent(points.size());
    for (int x = 0; x < points.size(); ++x) {
        parent[x] = x;
    }
    int last_index1 = -1;
    int last_index2 = -1;
    while (!min_heap.empty()) {
        DistancePair dist_pair = min_heap.top();
        min_heap.pop();
        if (find(dist_pair.index1, parent) != find(dist_pair.index2, parent)) {
            last_index1 = dist_pair.index1;
            last_index2 = dist_pair.index2;
            union_sets(dist_pair.index1, dist_pair.index2, parent);
        }
    }
    return to_string(points[last_index1].x * points[last_index2].x);
}

int main(int argc, char* argv[]) {
    solve(argv, part1, part2);
    return 0;
}