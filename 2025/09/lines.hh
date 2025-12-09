#include <array>
#include <cassert>
#include <iostream>

// helper class which holds a line segment, and can check whether it crosses
// another line segment.
struct Line {
    Line(std::pair<int, int> p1, std::pair<int, int> p2)
    : x0(p1.first)
    , y0(p1.second)
    , x1(p2.first)
    , y1(p2.second)
    {}
    int x0, y0, x1, y1;
};

bool line_cross(Line l1, Line l2) {
    bool l1_horizontal = (l1.y0 == l1.y1);
    bool l2_horizontal = (l2.y0 == l2.y1);
    if ((l1_horizontal and l2_horizontal) or (!l1_horizontal and !l2_horizontal)) {
        // if the lines are parallel they won't cross
        return false;
    }
    if (l1_horizontal) {
        // l1 is horizontal, l2 is vertical
        return (l1.x0 < l2.x0 and l1.x1 > l2.x0) and (l2.y0 < l1.y0 and l2.y1 > l1.y0);
    } else {
        // l1 is vertical, l2 is horizontal
        return (l2.x0 < l1.x0 and l2.x1 > l1.x0) and (l1.y0 < l2.y0 and l1.y1 > l2.y0);
    }
}

// does the line l cross the intersection of the joined line segments p1 and p2?
bool node_cross(Line p1, Line p2, Line l) {
    assert (p1.x1 == p2.x0 and p1.y1 == p2.y0); // establish the order
    // check if the node is on the line segment
    const int nodex = p1.x1;
    const int nodey = p1.y1;
    if ((nodex < std::min(l.x0, l.x1) or nodex > std::max(l.x0, l.x1))) {
        // the node is outside the x of the line segment
        return false;
    }
    if (nodey < std::min(l.y0, l.y1) or nodey > std::max(l.y0, l.y1)) {
        // the node is outside the y range of the line segment
        return false;
    }
    if ((nodex - l.x0) * (l.y1 - l.y0) - (nodey - l.y0) * (l.x1 - l.x0) != 0) {
        // this means the node does not lie on the line by the determinant
        return false;
    }

    // check with cross products whether the line crosses the path or not
    float cross1 = (l.x1 - l.x0) * (p1.y1 - p1.y0) - (p1.x1 - p1.x0) * (l.y1 - l.y0);
    float cross2 = (l.x1 - l.x0) * (p2.y1 - p2.y0) - (p2.x1 - p2.x0) * (l.y1 - l.y0);
    return ((cross1 > 0 and cross2 > 0) or (cross1 < 0 and cross2 < 0));

}

void test_lines_helper() {
    // trivial maths since lines are horizontal or vertical, check line_cross
    assert (false == line_cross({{0,2},{5,2}}, {{5,2},{10,2}})); // end to end
    assert (false == line_cross({{0,2},{5,2}}, {{4,2},{4,5}})); // end to side
    assert (false == line_cross({{0,2},{5,2}}, {{4,2},{7,2}})); // parallel and coincident
    assert (true == line_cross({{0,2},{5,2}}, {{4,0},{4,7}})); // cross one way
    assert (true == line_cross({{2,-2},{2,2}}, {{1,1},{3,1}})); // cross the other way

    // check node_cross
    assert (true == node_cross({{0, 0},{4, 4}}, {{4, 4},{6, 5}}, {{4, 0},{4, 8}}));
    assert (false == node_cross({{0, 0},{4, 4}}, {{4, 4},{3, 6}}, {{4, 0},{4, 8}}));
}
