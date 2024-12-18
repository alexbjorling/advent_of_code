/*
 * Desperate attempt to brute force part 2 as I was too confused about the program.
 * We know the number is between 8**15 and 8**16, since the output is length 16.
 */

#include <cmath>
#include <iostream>

using namespace std;

uint64_t program[] = {2,4,1,3,7,5,1,5,0,3,4,1,5,5,3,0};

int main() {
    uint64_t a, b, c;
    uint64_t output[16];
    bool ok;

    for (uint64_t i = pow(8, 15); i < pow(8, 16); i++) {
        a = i;
        ok = true;
        for (size_t j = 0; j < 16; j++) {
            b = a % 8;
            b = b ^ 3;
            c = a >> b;
            b = b ^ 5;
            a = a >> 3;
            b = b ^ 3;
            if (b % 8 != program[j]) {
                ok = false;
                break;
            }
        }
        if (ok) {
            cout << "found it! " << i << endl;
        }
    }
    return 0;
}
