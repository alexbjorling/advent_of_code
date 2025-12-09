//#include <algorithm>
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
    auto tiles = load("input.txt");
    std::vector<long> areas;
    for (size_t i = 0; i < tiles.size(); i++) {
        for (size_t j = 0; j < i; j++) {
            areas.push_back(tiles[j] - tiles[i]);
        }
    }
    long ans = *std::max_element(areas.cbegin(), areas.cend());
    assert(ans == 4740155680);
    return 0;
}
