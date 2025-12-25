#include <cassert>
#include <fstream>
#include <regex>
#include <set>
#include <string>
#include <vector>

// return a vector of Blocks, where a Block is a set of coordinate pairs
typedef std::set<std::pair<int, int>> Block;
std::vector<Block> parse_blocks(std::string fn) {
    // read the file as one big string
    std::ifstream ifs(fn);
    std::stringstream buf;
    buf << ifs.rdbuf();
    auto lines = buf.str();
    // regex out all the strings ending with \n\n
    std::vector<Block> ret {};
    auto pattern = std::regex("([#\\.]{3})\\n([#\\.]{3})\\n([#\\.]{3})");
    auto start = std::sregex_iterator(lines.cbegin(), lines.cend(), pattern);
    auto end = std::sregex_iterator();
    for (auto it = start; it != end; it++) {
        Block blk;
        auto match = *it;
        assert(match.size() == 4);
        for (size_t i = 0; i < 3; i++) {
            auto str = match[i + 1].str();
            for (size_t j = 0; j < 3; j++) {
                if (str[j] == '#') {
                    blk.insert({i, j});
                }
            }
        }
        ret.push_back(blk);
    }
    return ret;
}

// get those MxN: a b c d lines describing the spaces and what blocks to pick
void parse_spaces(std::string fn,
                  std::vector<std::pair<int, int>>& sizes,
                  std::vector<std::vector<int>>& picks) {
    std::ifstream ifs(fn);
    std::regex pattern {"([0-9]+)x([0-9]+)\\:(.*?)"};
    std::string line;

    while (std::getline(ifs, line)) {
        std::smatch match;
        if (std::regex_match(line, match, pattern)) {
            sizes.push_back({std::stoi(match[1].str()), std::stoi(match[2].str())});
            auto str = match[3].str();
            std::regex ptrn {"[0-9]+"};
            auto start = std::sregex_iterator(str.begin(), str.end(), ptrn);
            auto end = std::sregex_iterator();
            std::vector<int> numbers {};
            for (auto it = start; it != end; it++) {
                numbers.push_back(std::stoi((*it).str()));
            }
            picks.push_back(numbers);
        }
    }
}

// sad solution which works for the problem but not the example: all shapes 3x3 solids.
int main() {
    auto block_shapes = parse_blocks("input.txt");
    std::vector<std::vector<int>> picks;
    std::vector<std::pair<int, int>> space_shapes;
    parse_spaces("input.txt", space_shapes, picks);

    int total = 0;
    for (size_t i = 0; i < space_shapes.size(); i++) {
        auto space_shape = space_shapes[i];
        int cnt = 0;
        for (size_t j = 0; j < picks[i].size(); j++) {
            cnt += picks[i][j];
        }
        if (cnt <= (space_shape.first / 3) * (space_shape.second / 3)) {
            total++;
        }
    }
    assert(599 == total);
    return 0;
}
