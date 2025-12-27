#include <cassert>
#include <fstream>
#include <regex>
#include <set>
#include <string>
#include <vector>

#include <iostream>

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
int main_() {
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


// below is a brute force solution which solves the example

// first some helpers - to flip a block
Block flip(const Block& block) {
    Block ret {};
    for (auto& pt : block) {
        ret.insert({2 - pt.first, pt.second});
    }
    return ret;
}

// to rotate one recursively
Block rotate(Block block, int times) {
    if (times == 0) {
        return block;
    } else {
        Block rotated {};
        for (auto& pt : block) {
            rotated.insert({pt.second, 2 - pt.first});
        }
        return rotate(rotated, times - 1);
    }
}

// to translate a block in x and y
Block translate(Block block, int dx, int dy) {
    Block ret {};
    for (auto& pt : block) {
        ret.insert({pt.first + dx, pt.second + dy});
    }
    return ret;
}

// to render it to screen nicely
void render_block(Block block, std::pair<int, int> space) {
    std::vector<std::string> board;
    for (size_t i = 0; i < space.second; i++) {
        std::string str(space.first, '.');
        board.push_back(str);
    }
    for (auto& pt : block) {
        board[pt.second][pt.first] = '#';
    }
    for (auto& row : board) {
        std::cout << row << std::endl;
    }
    std::cout << std::endl;
}

// to check if one block overlaps with another
bool overlap(const Block& b1, const Block& b2) {
    for (auto& pt : b2) {
        if (b1.count(pt)) {
            return true;
        }
    }
    return false;
}

// then the main recursive function which brute-forces the problem recursively
bool place(std::vector<int> pieces, const std::vector<Block>& piece_shapes, const std::pair<int, int>& space, Block busy) {
    if (pieces.size() == 0) {
        // no more pieces to place, we are done!
        render_block(busy, space);
        return true;
    }

    // take a piece from the queue and make an update queue copy
    int next = pieces[0];
    std::vector<int> queue(pieces.cbegin() + 1, pieces.cend());

    // try to place the piece in all possible ways, and recurse when possible
    for (int x = 0; x < space.first - 2; x++) {
        for (int y = 0; y < space.second - 2; y++) {
            for (int rot = 0; rot < 4; rot++) {
                for (int mirror = 0; mirror < 2; mirror++) {
                    // translate, rotate, flip, then test against the busy board
                    auto block{piece_shapes[next]};
                    block = mirror ? flip(block) : block;
                    block = rotate(block, rot);
                    block = translate(block, x, y);
                    if (!overlap(busy, block)) {
                        Block new_busy(busy);
                        new_busy.merge(block);
                        if (place(queue, piece_shapes, space, new_busy)) {
                            return true;
                        }
                    }
                }
            }
        }
    }
    return false;
}

int main() {
    auto block_shapes = parse_blocks("ex.txt");
    std::vector<std::vector<int>> picks;
    std::vector<std::pair<int, int>> space_shapes;
    parse_spaces("ex.txt", space_shapes, picks);
    assert(space_shapes.size() == picks.size());

    int total = 0;
    for (size_t i = 0; i < space_shapes.size(); i++) {
        // render a list of pieces
        std::vector<int> pieces;
        for (int j = 0; j < picks[i].size(); j++) {
            for (int n = 0; n < picks[i][j]; n++) {
                pieces.push_back(j);
            }
        }
        // call the recursive piece placement function
        Block busy {};
        total += place(pieces, block_shapes, space_shapes[i], busy);
    }
    std::cout << total << std::endl;
    //assert(599 == total);
    return 0;
}
