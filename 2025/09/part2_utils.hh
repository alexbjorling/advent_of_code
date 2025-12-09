#include <algorithm>
#include <cassert>
#include <vector>

// helper class to store positions and take distances
struct Point {
    int x, y;
    Point() {};
    Point(long x_, long y_) : x(x_), y(y_) {};
    bool operator==(Point& other) {
        return (x == other.x and y == other.y);
    }
};

// what's the area covered by a rectangle of tiles with corners at p1 and p2?
long tile_area(Point& p1, Point& p2) {
    return (std::abs(p2.x - p1.x) + 1) * static_cast<long>((std::abs(p2.y - p1.y) + 1));
}

// helper class which holds a line segment (horizontal or vertical)
struct Line {
    Line(std::pair<int, int> p1, std::pair<int, int> p2)
    : x0(p1.first)
    , y0(p1.second)
    , x1(p2.first)
    , y1(p2.second)
    {
        horizontal = (y0 == y1);
        if (horizontal) {
            assert(x0 != x1);
        }
    }
    int x0, y0, x1, y1;
    bool contains(Point p) const {
        if (horizontal) {
            return (p.y == y0 and (p.x >= std::min(x0, x1) and p.x <= std::max(x0, x1)));
        } else {
            return (p.x == x0 and (p.y >= std::min(y0, y1) and p.y <= std::max(y0, y1)));
        }
    }
private:
    bool horizontal;
};

// return all the tiles that lie on the border of the rectangle spanned by,
// p1 and p2, inclusive.
std::vector<Point> render_tile_border(Point& p1, Point& p2) {
    int w = std::abs(p1.x - p2.x);
    int h = std::abs(p1.y - p2.y);
    std::vector<Point> ret {};
    ret.reserve(2 * w + 2 * h);
    int dx = (p2.x > p1.x) ? 1 : -1;
    int dy = (p2.y > p1.y) ? 1 : -1;
    for (long i = 0; i <= w; i++) {
        ret.push_back({p1.x + i * dx, p1.y});
    }
    for (long i = 0; i <= w; i++) {
        ret.push_back({p1.x + i * dx, p2.y});
    }
    for (long i = 1; i < h; i++) {
        ret.push_back({p1.x, {p1.y + i * dy}});
    }
    for (long i = 1; i < h; i++) {
        ret.push_back({p2.x, {p1.y + i * dy}});
    }
    return ret;
}

bool point_outside_polygon(Point& p, const std::vector<Line>& polygon, long xmax) {
    int crossings = 0;
    int x = p.x;
    bool on_border;
    while (x <= xmax + 1) {
        for (auto& l : polygon) {
            on_border = l.contains({x, p.y});
        }
        // do something smart here to figure out if we've crossed a border
        x++;
    }
    crossings = 1; // tmp, means all points are inside
    return (crossings % 2) == 1;
}

void test_geometry() {
    Line lh({{0, 2}, {5, 2}});
    assert (false == lh.contains({3, 4}));
    assert (false == lh.contains({7, 2}));
    assert (true == lh.contains({0, 2}));
    assert (true == lh.contains({3, 2}));
    assert (true == lh.contains({5, 2}));

    Line lv({{5, 2}, {5, 7}});
    assert (false == lv.contains({3, 4}));
    assert (false == lv.contains({5, 0}));
    assert (true == lv.contains({5, 2}));
    assert (true == lv.contains({5, 5}));
    assert (true == lv.contains({5, 7}));

    Point p1 {1, 1};
    Point p2 {4, 3};
    auto border = render_tile_border(p1, p2);
    std::vector<Point> expected = {
        {1, 1}, {2, 1}, {3, 1}, {4, 1}, {1, 3}, {2, 3}, {3, 3}, {4, 3}, {1, 2}, {4, 2}
    };
    assert(border.size() == expected.size());
    for (size_t i = 0; i < expected.size(); i++) {
        assert (border[i] == expected[i]);
    }
}