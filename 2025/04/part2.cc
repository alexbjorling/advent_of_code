#include <cassert>
#include <fstream>
#include <stdexcept>
#include <string>
#include <unordered_set>

// this time we use unordered_set, so need a helper to hash pairs
struct HashPairHelper {
    size_t operator() (const std::pair<int, int>& input) const {
        auto h1 = std::hash<int>{}(input.first);
        auto h2 = std::hash<int>{}(input.second);
        return h1 ^ (h2 << 1); // xor
    }
};

// the specific set used
typedef std::unordered_set<std::pair<int, int>, HashPairHelper> set;

// helper to find rolls with fewer than N neighbors in the set of all rolls
set find_free_rolls(const set& positions, int N) {
    set ret {};
    set neighbors {{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};
    for (auto& pos : positions) {
        int neighbor_count = 0;
        for (auto& neigh : neighbors) {
            if (positions.count({neigh.first + pos.first, neigh.second + pos.second})) {
                neighbor_count++;
            }
        }
        if (neighbor_count < N) {
            ret.insert(pos);
        }
    }
    return ret;
}

int main() {
    // input
    std::ifstream ifs("input.txt");
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }

    // fish out a set of occupied positions, would be nice with an unordered set but pair<int, int> doesn't hash
    set positions {};
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

    // part 2: remove rolls repeatedly until no more can be removed
    int original_size = positions.size();
    int last_size = 0;
    while (last_size != positions.size()) {
        last_size = positions.size();
        auto loose = find_free_rolls(positions, 4);
        for (auto& it : loose) {
            positions.erase(it);
        }
    }
    assert (original_size - positions.size() == 9206);

    return 0;
}
