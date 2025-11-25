#include <fstream>
#include <string>
#include <cassert>
#include <map>

enum Sign { rock, paper, scissors };

std::map<char, Sign> sign_map {
    { 'A', Sign::rock },
    { 'B', Sign::paper },
    { 'C', Sign::scissors },
    { 'X', Sign::rock },
    { 'Y', Sign::paper },
    { 'Z', Sign::scissors },
};

std::map<Sign, int> score_map {
    { Sign::rock, 1 },
    { Sign::paper, 2 },
    { Sign::scissors, 3 },
};

int result(Sign them, Sign us) {
    if (us == them) {
        return 3;
    }
    bool win = (them == Sign::rock and us == Sign::paper)
        or (them == Sign::paper and us == Sign::scissors)
        or (them == Sign::scissors and us == Sign::rock);
    return win ? 6 : 0;
}

int main() {
    // open the file
    std::ifstream ifs("input.txt");
    if (ifs.fail()) {
        return -1;
    }

    // loop through the rounds
    std::string line;
    int sum = 0;
    while (std::getline(ifs, line)) {
        auto them = sign_map.at(line[0]);
        auto us = sign_map.at(line[2]);
        sum += result(them, us) + score_map.at(us);
    }
    assert (sum == 13221);
}