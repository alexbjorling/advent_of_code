#include "part2_utils.hh"

#include <cassert>
#include <fstream>
#include <regex>
#include <stdexcept>
#include <string>
#include <vector>

// open the input file and make a vector of boxes
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
    test_geometry();
    auto tiles = load("input.txt");

    // assemble a polygon to check against
    std::vector<Line> polygon;
    for (size_t i = 1; i < tiles.size(); i++) {
        polygon.push_back(Line({tiles[i-1].x, tiles[i-1].y}, {tiles[i].x, tiles[i].y}));
    }
    polygon.push_back(Line({tiles.back().x, tiles.back().y}, {tiles[0].x, tiles[0].y}));

    // loop through all the tile pairs, calculating the area and
    // sorting the options. this is quick.
    typedef std::pair<long, std::pair<size_t, size_t>> option;
    std::vector<option> options;
    for (size_t i = 0; i < tiles.size(); i++) {
        for (size_t j = 0; j < i; j++) {
            options.push_back({tile_area(tiles[i], tiles[j]), {i, j}});
        }
    }
    std::sort(options.begin(), options.end(), [](option& op1, option& op2){ return op1.first > op2.first; });

    // find a maximum x value for the PIP algorithm later
    std::vector<int> x {};
    for (auto& p : tiles) {
        x.push_back(p.x);
    }
    const int xmax = *std::max_element(x.cbegin(), x.cend());

    // loop through the options until we find an acceptable one
    long area = 0;
    for (auto& opt : options) {
        // find all the tiles on the rectangle border
        auto& t1 = tiles[opt.second.first];
        auto& t2 = tiles[opt.second.second];
        auto border = render_tile_border(t1, t2);

        // check if each lies on one of the polygon edges
        bool done = true;
        for (auto& b : border) {
            if (point_outside_polygon(b, polygon, xmax)) {
                done = false;
                break;
            }
        }

        if (done) {
            area = opt.first;
            break;
        }
    }

    printf("area = %ld\n", area);
    // line_cross fixes the example but gives the p1 answer for the input
    // 3197574321 high
    // 4555903716
    // 4740155680 part 1
    return 0;
}
