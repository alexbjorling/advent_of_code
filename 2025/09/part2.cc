#include "lines.hh"

#include <cassert>
#include <fstream>
#include <regex>
#include <stdexcept>
#include <string>
#include <vector>

// helper class to store positions and take distances
struct Tile {
    long x, y;
    // tile1 - tile2 gives the area spanned by the two tiles
    long operator-(const Tile& other) const {
        return std::abs((x - other.x + 1) * (y - other.y + 1));
    }
};

// open the input file and make a vector of boxes
std::vector<Tile> load(const std::string& fn) {
    std::ifstream ifs(fn);
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }
    std::vector<Tile> tiles {};
    std::string line;
    while (std::getline(ifs, line)) {
        std::smatch match;
        std::regex pattern {"([0-9]+),([0-9]+)"};
        std::regex_match(line, match, pattern);
        Tile tile {};
        tile.x = std::stoi(match[1].str());
        tile.y = std::stoi(match[2].str());
        tiles.push_back(tile);
    }
    return tiles;
}

int main() {
    test_lines_helper();
    auto tiles = load("ex.txt");

    // assemble a polygon to check agains
    std::vector<Line> polygon;
    for (size_t i = 1; i < tiles.size(); i++) {
        polygon.push_back(Line({tiles[i-1].x, tiles[i-1].y}, {tiles[i].x, tiles[i].y}));
    }
    polygon.push_back(Line({tiles.back().x, tiles.back().y}, {tiles[0].x, tiles[0].y}));

    // loop through all the
    std::vector<long> areas;
    for (size_t i = 0; i < tiles.size(); i++) {
        for (size_t j = 0; j < i; j++) {
            // the edges of the current rectangle
            Line l1 ({tiles[i].x, tiles[i].y}, {tiles[i].x, tiles[j].y});
            Line l2 ({tiles[i].x, tiles[j].y}, {tiles[j].x, tiles[j].y});
            Line l3 ({tiles[j].x, tiles[j].y}, {tiles[j].x, tiles[i].y});
            Line l4 ({tiles[i].x, tiles[i].y}, {tiles[j].x, tiles[i].y});

            // is this a valid rectangle?
            bool skip = false;
            for (size_t k = 0; k < polygon.size(); k++) {
                // do any of the rectangle edges intersect this polygon edge?
                const Line& p = polygon[k];
                if (line_cross(p, l1) or line_cross(p, l2) or line_cross(p, l3) or line_cross(p, l4)) {
                    skip = true;
                    break;
                }

                // do any of the rectangle edges cross the polygon at one of its corners?
                const Line& p1 = (k == polygon.size() - 1) ? polygon[0] : polygon[k+1];
                if (node_cross(p, p1, l1) or node_cross(p, p1, l2) or node_cross(p, p1, l3) or node_cross(p, p1, l4)) {
                    skip = true;
                    break;
                }
            }
            if (skip) { continue; }
            // if yes, add the candidate area
            areas.push_back(tiles[j] - tiles[i]);
        }
    }
    long ans = *std::max_element(areas.cbegin(), areas.cend());
    printf("** %ld\n", ans);
    // line_cross fixes the example but gives the p1 answer for the input
    // 3197574321 high
    // 4555903716
    // 4740155680 part 1
    return 0;
}
