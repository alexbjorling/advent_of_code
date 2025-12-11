#include <fstream>
#include <regex>
#include <stdexcept>
#include <string>

std::vector<int> comma_split(const std::string& s) {
    std::regex numbers("[0-9]+");
    auto b = std::sregex_iterator(s.cbegin(), s.cend(), numbers);
    auto e = std::sregex_iterator();
    std::vector<int> elements {};
    for (auto it_ = b; it_ != e; it_++) {
        elements.push_back(std::stoi((*it_).str()));
    }
    return elements;
}

// the worst parser ever
typedef std::tuple<std::vector<int>, std::vector<std::vector<int>>, std::vector<int>> Row;
std::vector<Row> load_data(std::string fn) {
    // make a return container
    std::vector<Row> rows;
    // load the file line by line
    std::ifstream ifs("ex.txt");
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }
    std::string line;
    while (std::getline(ifs, line)) {
        Row row {};

        // find the [] contained string
        {
            std::regex pattern("\\[(.*)\\]");
            std::smatch match;
            std::regex_search(line, match, pattern);
            for (char& c : match[1].str()) {
                if (c == '#') {
                    std::get<0>(row).push_back(1);
                } else if (c == '.') {
                    std::get<0>(row).push_back(0);
                } else {
                    throw std::runtime_error("unexpected character in [] string");
                }
            }
        }

        // find a set of parentheses and the numbers in them, then return basis vectors
        std::regex pattern("(\\(.+?\\))"); // non greedy
        auto begin = std::sregex_iterator(line.cbegin(), line.cend(), pattern);
        auto end = std::sregex_iterator();
        for (auto it = begin; it != end; it++) {
            auto match = *it;
            auto str = match.str();
            auto indices = comma_split(str);
            std::vector<int> elements(std::get<0>(row).size(), 0);
            for (auto& ind : indices) {
                elements[ind] = 1;
            }
            std::get<1>(row).push_back(elements);
        }

        // find the {} contained string and the numbers in them
        {
            std::regex pattern("\\{(.*)\\}");
            std::smatch match;
            std::regex_search(line, match, pattern);
            auto elements = comma_split(match[1].str());
            std::get<2>(row) = elements;
        }

        rows.push_back(row);
    }
    return rows;
}