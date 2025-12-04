#include <cassert>
#include <fstream>
#include <stdexcept>
#include <string>
#include <set>

int main() {
    // input
    std::ifstream ifs("input.txt");
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }

    // fish out a set of occupied positions, would be nice with an unordered set but pair<int, int> doesn't hash
    std::set<std::pair<int, int>> positions {};
    std::string line;
    size_t i = 0;
    while (std::getline(ifs, line)) {
        for (size_t j = 0; j < line.size(); j++) {
            if (line[j] == '@') {
                positions.emplace(i, j);
            }
        }
        i++;
    }

    // part1: see how many rolls have fewer than 4 neighbors
    int cnt = 0;
    std::set<std::pair<int, int>> neighbors {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};
    for (auto& pos : positions) {
        int neighbor_count = 0;
        for (auto& neigh : neighbors) {
            if (positions.count({neigh.first + pos.first, neigh.second + pos.second})) {
                neighbor_count++;
            }
        }
        if (neighbor_count < 4) {
            cnt++;
        }
    }
    assert(cnt == 1533);

    return 0;
}
