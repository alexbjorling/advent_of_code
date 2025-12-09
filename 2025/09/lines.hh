#include <array>
#include <cassert>

// helper class which holds a line segment, and can check whether it crosses
// another line segment.
class Line {
public:
    Line(std::pair<int, int> p1, std::pair<int, int> p2)
    : x0(p1.first)
    , y0(p1.second)
    , x1(p2.first)
    , y1(p2.second)
    {}

    // use the + operator to return whether the lines cross or not,
    // with one line ending on the other is not considered a cross
    bool operator+(Line& other) {
        // parametrize the lines a and b,
        // with a0 = (x0, y0), a1 = (x1, xy) for line as, and vice versa
        // then set
        // a0 + ta * (a1 - a0) = b0 + tb * (b1 - b0) and solve for (ta, tb)

        // A = t * b, where
        const std::array<std::array<int, 2>, 2> A {{
            {x1 - x0, other.x1 - other.x0},
            {y1 - y0, other.y1 - other.y0}
        }};
        const std::array<std::array<int, 2>, 2> B {{
            {1, 2},
            {3, 4}
        }};
        // and
        std::array<int, 2> b {other.x0 - x0, other.y0 - y0};

        // get and check the determinant
        int det = A[0][0] * A[1][1] - A[0][1] * A[1][0];
        if (det == 0) {
            // lines are parallel
            return 0;
        }

        // find the inverse matrix
        double d = 1.0 / det;
        const std::array<std::array<double, 2>, 2> Ainv {{
            {A[1][1] * d, -A[0][1] * d},
            {-A[1][0] * d, A[0][0] * d}
        }};

        // solve for the parameters and check for crossing
        double ta = b[0] * Ainv[0][0] + b[1] * Ainv[0][1];
        double tb = -(b[0] * Ainv[1][0] + b[1] * Ainv[1][1]);
        return (ta > 0 and ta < 1 and tb > 0 and tb < 1);
    }

    // equality operator
    bool operator==(Line& other) {
        return (x0 == other.x0 and y0 == other.y0 and x0 == other.x0 and x1 == other.x1);
    }
private:
    int x0, y0, x1, y1;
};

bool check_lines(Line l1, Line l2) {
        return l1 + l2;
    }

void test_algebra() {
    assert (true == check_lines({{0,0},{5,5}}, {{0,2},{5,2}}));
    assert (false == check_lines({{0,0},{5,5}}, {{1,1},{5,1}})); // false (meet but don't cross)
    assert (false == check_lines({{0,0},{5,5}}, {{2,1},{5,1}})); // false
    assert (false == check_lines({{0,0},{5,0}}, {{0,2},{5,2}})); // false, parallel
    assert (true == check_lines({{0,0},{5,0}}, {{2,-2},{2,2}})); // true
}
