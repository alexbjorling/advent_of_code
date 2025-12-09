#include <algorithm> // min, max, abs
#include <cassert>
#include <fstream>
#include <regex>
#include <stdexcept>
#include <string>
#include <vector>

// helper class to store positions
struct Point {
    int x, y;
    Point() {};
    Point(long x_, long y_) : x(x_), y(y_) {};
};

// helper class which holds a line segment (horizontal or vertical)
struct Line {
    Line(std::pair<int, int> p1, std::pair<int, int> p2)
    : x0(p1.first)
    , y0(p1.second)
    , x1(p2.first)
    , y1(p2.second)
    {}
    int x0, y0, x1, y1;
};

// what's the area covered by a rectangle of tiles with corners at p1 and p2?
long tile_area(Point& p1, Point& p2) {
    return (std::abs(p2.x - p1.x) + 1) * static_cast<long>((std::abs(p2.y - p1.y) + 1));
}

// helper to open the input file and make a vector of points where the tiles are
std::vector<Point> load(const std::string& fn) {
    std::ifstream ifs(fn);
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }
    std::vector<Point> tiles {};
    std::string line;
    while (std::getline(ifs, line)) {
        std::smatch match;
        std::regex pattern {"([0-9]+),([0-9]+)"};
        std::regex_match(line, match, pattern);
        Point tile {};
        tile.x = std::stoi(match[1].str());
        tile.y = std::stoi(match[2].str());
        tiles.push_back(tile);
    }
    return tiles;
}

int main() {
    auto tiles = load("input.txt");

    // assemble a polygon that our rectangle has to fit in
    std::vector<Line> polygon;
    for (size_t i = 1; i < tiles.size(); i++) {
        polygon.push_back(Line({tiles[i-1].x, tiles[i-1].y}, {tiles[i].x, tiles[i].y}));
    }
    polygon.push_back(Line({tiles.back().x, tiles.back().y}, {tiles[0].x, tiles[0].y}));

    // loop through all the tile pairs, calculating the area and sorting the
    // candidate pairs. this is quick.
    typedef std::pair<long, std::pair<size_t, size_t>> option;
    std::vector<option> options;
    for (size_t i = 0; i < tiles.size(); i++) {
        for (size_t j = 0; j < i; j++) {
            options.push_back({tile_area(tiles[i], tiles[j]), {i, j}});
        }
    }
    std::sort(options.begin(), options.end(), [](option& op1, option& op2){ return op1.first > op2.first; });

    // loop through the options until we find the first acceptable one
    long area = 0;
    for (auto& opt : options) {
        // check if the polygon line segment is found inside the rectangle. since
        // everything is horizontal or vertical, this is enough.
        bool done = true;
        auto& t1 = tiles[opt.second.first];
        auto& t2 = tiles[opt.second.second];
        for (auto& p : polygon) {
            bool in_rect = std::min(p.x0, p.x1) < std::max(t1.x, t2.x)
                           and std::max(p.x0, p.x1) > std::min(t1.x, t2.x)
                           and std::min(p.y0, p.y1) < std::max(t1.y, t2.y)
                           and std::max(p.y0, p.y1) > std::min(t1.y, t2.y);
            if (in_rect) {
                done = false;
                break;
            }
        }

        if (done) {
            area = opt.first;
            break;
        }
    }

    assert(area == 1543501936);
    return 0;
}
