
#include <algorithm>
#include <cmath>
#include <iostream>
#include <map>
#include <ranges>
#include <sstream>
#include <string>
#include <vector>

#include "utils.h"

using namespace std;

struct Point {
    long long x;
    long long y;

    bool operator<(const Point &other) const {
        if (x != other.x) {
            return x < other.x;
        }
        return y < other.y;
    }
};

const string part1(const string &input) {
    vector<string> lines = split_string(input);

    long long x, y;
    char comma;
    vector<Point> points;
    for (const auto &line : lines) {
        stringstream ss(line);
        ss >> x >> comma >> y;
        points.push_back(Point{x, y});
    }
    long long max_area = 0;
    for (int i = 0; i < points.size(); ++i) {
        for (int j = i + 1; j < points.size(); ++j) {
            long long area =
                (abs(points[i].x - points[j].x) + 1) * (abs(points[i].y - points[j].y) + 1);
            max_area = max(max_area, area);
        }
    }
    return to_string(max_area);
}

long long cross_product(Point a, Point b, Point c) {
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

bool is_on_segment(Point p, Point a, Point b) {
    if (cross_product(a, b, p) != 0) return false;
    return (p.x >= min(a.x, b.x) && p.x <= max(a.x, b.x) && p.y >= min(a.y, b.y) &&
            p.y <= max(a.y, b.y));
}

bool is_point_inside(Point p, const vector<Point> &polygon, map<Point, bool> &memo) {
    if (memo.find(p) != memo.end()) {
        return memo[p];
    }
    int n = polygon.size();
    bool inside = false;
    for (int i = 0; i < n; i++) {
        Point p1 = polygon[i];
        Point p2 = polygon[(i + 1) % n];
        if (is_on_segment(p, p1, p2)) {
            return true;
        }
        bool is_y_spanning = (p1.y > p.y) != (p2.y > p.y);
        if (is_y_spanning) {
            long long cp = cross_product(p1, p2, p);
            if (p2.y > p1.y) {
                if (cp > 0) inside = !inside;
            } else {
                if (cp < 0) inside = !inside;
            }
        }
    }
    memo[p] = inside;
    return inside;
}

vector<Point> rectangle_boundary(Point p1, Point p2) {
    vector<Point> boundary;
    long long min_x = min(p1.x, p2.x);
    long long max_x = max(p1.x, p2.x);
    long long min_y = min(p1.y, p2.y);
    long long max_y = max(p1.y, p2.y);

    for (long long x = min_x; x <= max_x; ++x) {
        boundary.push_back(Point{x, min_y});
        boundary.push_back(Point{x, max_y});
    }
    for (long long y = min_y + 1; y < max_y; ++y) {
        boundary.push_back(Point{min_x, y});
        boundary.push_back(Point{max_x, y});
    }
    return boundary;
}

const string part2(const string &input) {
    vector<string> lines = split_string(input);

    long long x, y;
    char comma;
    vector<Point> points;
    for (const auto &line : lines) {
        stringstream ss(line);
        ss >> x >> comma >> y;
        points.push_back(Point{x, y});
    }

    long long max_area = 0;
    map<Point, bool> memo;
    for (int i = 0; i < points.size(); ++i) {
        cout << i << endl;
        for (int j = i + 1; j < points.size(); ++j) {
            long long area =
                (abs(points[i].x - points[j].x) + 1) * (abs(points[i].y - points[j].y) + 1);
            if (area <= max_area) {
                continue;
            }
            vector<Point> boundary = rectangle_boundary(points[i], points[j]);
            bool all_inside = true;
            for (const auto &p : boundary) {
                if (!is_point_inside(p, points, memo)) {
                    all_inside = false;
                    break;
                }
            }
            if (!all_inside) {
                continue;
            }
            max_area = area;
        }
    }

    return to_string(max_area);
}

int main(int argc, char *argv[]) {
    solve(argv, part1, part2);
    return 0;
}