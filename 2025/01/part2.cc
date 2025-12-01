#include <cassert>
#include <fstream>
#include <stdexcept>
#include <string>

class Dial {
public:
    Dial() : pos(50) {};

    int move(int mv) {
        // start with the whole cycles of 100
        int crossings = std::abs(mv / 100);
        pos = (pos + (mv / 100) * 100) % 100;
        // then loop for the rest, mv % 100 left to go
        int sign = (mv % 100) / std::abs(mv % 100);
        for (size_t i = 0; i < std::abs(mv % 100); i++) {
            pos += sign;
            crossings += (pos % 100 == 0);
        }
        return crossings;
    }

    int move(const std::string& str) {
        int sign = (str[0] == 'L') ? -1 : 1;
        auto dist = std::string(str.begin() + 1, str.end());
        auto distn = std::stoi(dist);
        return move(sign * distn);
    }

private:
    int pos;
};

int main() {
    std::ifstream ifs("input.txt");
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }

    Dial d;
    std::string move;
    int counts = 0;
    while (std::getline(ifs, move)) {
        counts += d.move(std::string(move));
    }
    assert(counts == 6228);
    return 0;
}
