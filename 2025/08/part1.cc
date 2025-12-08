#include <algorithm>
#include <cassert>
#include <fstream>
#include <regex>
#include <stdexcept>
#include <string>
#include <vector>

// helper class to store positions and take distances
struct Box {
    long x, y, z;
    // box1 - box2 gives the square distance between the two boxes
    long operator-(const Box& other) const {
        return (x - other.x) * (x - other.x)
               + (y - other.y) * (y - other.y)
               + (z - other.z) * (z - other.z);
    }
    // == and != operators for std::find
    bool operator==(const Box& other) const {
        return (x == other.x and y == other.y and z == other.z);
    }
    bool operator!=(const Box& other) const {
        return (x != other.x or y != other.y or z != other.z);
    }
};

// open the input file and make a vector of boxes
std::vector<Box> load(const std::string& fn) {
    std::ifstream ifs(fn);
    if (ifs.fail()) {
        throw std::runtime_error("Failed to open input file");
    }
    std::vector<Box> boxes {};
    std::string line;
    while (std::getline(ifs, line)) {
        std::smatch match;
        std::regex pattern {"([0-9]+),([0-9]+),([0-9]+)"};
        std::regex_match(line, match, pattern);
        Box box {};
        box.x = std::stoi(match[1].str());
        box.y = std::stoi(match[2].str());
        box.z = std::stoi(match[3].str());
        for (auto& b : boxes) {
            assert(b != box);
        }
        boxes.push_back(box);
    }
    return boxes;
}

int main() {
    auto boxes = load("input.txt");

    // now make a vector of all the possible connections as <distance, <box1, box2>>
    typedef std::pair<long, std::pair<Box, Box>> couple;
    std::vector<couple> distances;
    for (size_t i = 0; i < boxes.size(); i++) {
        for (size_t j = 0; j < i; j++) {
            distances.push_back({boxes[i] - boxes[j], {boxes[i], boxes[j]}});
        }
    }

    // sort that vector in place based on just the distance, so we know in what order
    // to pick the pairs
    std::sort(distances.begin(), distances.end(),
              [](couple& c1, couple& c2) {return c1.first < c2.first;});

    // start with each box in its own circuit
    std::vector<std::vector<Box>> circuits;
    for (auto& b : boxes) {
        circuits.push_back({b,});
    }

    // make 1000 connections
    for (size_t i = 0; i < 1000; i++) {
        // see if any of our two boxes are present in any of the existing circuits
        int b1_circuit, b2_circuit;
        const auto& box1 = distances[i].second.first;
        const auto& box2 = distances[i].second.second;
        for (size_t j = 0; j < circuits.size(); j++) {
            if (std::find(circuits[j].begin(), circuits[j].end(), box1) != circuits[j].end()) {
                b1_circuit = j;
            }
            if (std::find(circuits[j].begin(), circuits[j].end(), box2) != circuits[j].end()) {
                b2_circuit = j;
            }
        }

        // now there are a few cases to handle
        if (b1_circuit != b2_circuit) {
            // both are connected in different circuits, merge these sets into b1_circuit
            for (auto& it : circuits[b2_circuit]) {
                circuits[b1_circuit].push_back(it);
            }
            circuits.erase(circuits.begin() + b2_circuit);
        }
    }

    // then sort the vector of circuits according to their sizes
    auto size = [](std::vector<Box>& c1, std::vector<Box>& c2) { return c1.size() > c2.size(); };
    std::sort(circuits.begin(), circuits.end(), size);
    long ans = circuits[0].size() * circuits[1].size() * circuits[2].size();
    assert (ans == 54180);

    return 0;
}
