#include <cassert>
#include <fstream>
#include <stdexcept>
#include <string>

class Dial {
public:
    Dial() : pos(50) {};

    int move(int mv) {
        int sign = mv / std::abs(mv);
        int crossings = 0;
        for (size_t i = 0; i < std::abs(mv); i++) {
            pos += sign;
            if (pos % 100 == 0) {
                crossings++;
            }
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
