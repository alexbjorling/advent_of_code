#include <cassert>
#include <fstream>
#include <regex>
#include <stdexcept>
#include <string>
#include <vector>

// helper to load the file
std::string load(std::string fn) {
    std::ifstream ifs(fn);
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }
    std::stringstream buf;
    buf << ifs.rdbuf();
    std::string data(buf.str());
    return data;
}

// helper to parse a set of ints
std::vector<int> parse_ints(std::string& data) {
    std::vector<int> ret {};
    std::regex pattern("([0-9]+)\\s");
    auto begin = std::sregex_iterator(data.cbegin(), data.cend(), pattern);
    auto end = std::sregex_iterator();
    for (auto it = begin; it != end; it++) {
        auto match = *it;
        ret.push_back(std::stoi(match[0].str())); // index 0 is the whole match
    }
    return ret;
}

// helper to parse the operators
std::string parse_operators(std::string& data) {
    std::string ret {};
    std::regex pattern("([+*]+)");
    auto begin = std::sregex_iterator(data.cbegin(), data.cend(), pattern);
    auto end = std::sregex_iterator();
    for (auto it = begin; it != end; it++) {
        auto match = *it;
        ret.push_back(match[0].str()[0]); // index 0 is the whole match
    }
    return ret;
}

int main() {
    // load the file as one long string
    auto data = load("input.txt");

    // fish out all the numbers and operators
    auto numbers = parse_ints(data);
    auto operators = parse_operators(data);

    // collect the results in a vector
    size_t N = operators.size();
    std::vector<long> results;
    results.resize(N);

    // trick: first put ones in the result vector where there are multiplications
    for (size_t i = 0; i < N; i++) {
        results[i % N] = (operators[i % N] == '*') ? 1 : 0;

    }
    // then do the operations
    for (size_t i = 0; i < numbers.size(); i++) {
        if (operators[i % N] == '*') {
            results[i % N] *= numbers[i];
        } else if (operators[i % N] == '+') {
            results[i % N] += numbers[i];
        } else {
            throw std::runtime_error("Unexpected operator");
        }
    }

    // then sum and check
    long tot = 0;
    for (auto& n : results) {
        tot += n;
    }
    assert (tot == 5346286649122);

    return 0;
}
