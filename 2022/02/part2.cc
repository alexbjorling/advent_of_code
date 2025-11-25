#include <fstream>
#include <string>
#include <cassert>
#include <map>

enum Sign { rock, paper, scissors };
enum Result { lose, draw, win };

std::map<char, Sign> sign_map {
    { 'A', Sign::rock },
    { 'B', Sign::paper },
    { 'C', Sign::scissors },
};

std::map<char, Result> result_map {
    { 'X', Result::lose },
    { 'Y', Result::draw },
    { 'Z', Result::win },
};

std::map<Sign, int> sign_score_map {
    { Sign::rock, 1 },
    { Sign::paper, 2 },
    { Sign::scissors, 3 },
};

std::map<Result, int> result_score_map {
    { Result::lose, 0 },
    { Result::draw, 3 },
    { Result::win, 6 },
};

std::map<Sign, Sign> win_map {
    { Sign::rock, Sign::paper },
    { Sign::paper, Sign::scissors },
    { Sign::scissors, Sign::rock },
};

int main() {
    // work out the reverse of the win map
    std::map<Sign, Sign> lose_map;
    for (auto& it : win_map) {
        lose_map.insert({it.second, it.first});
    }

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
        auto result = result_map.at(line[2]);
        Sign us;
        if (result == Result::draw) {
            us = them;
        } else if (result == Result::win) {
            us = win_map.at(them);
        } else {
            us = lose_map.at(them);
        }
        sum += result_score_map.at(result) + sign_score_map.at(us);
    }
    assert (sum == 13131);
}