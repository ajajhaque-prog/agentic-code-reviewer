// bad_cpp.cpp
// C++ sample with unsafe patterns and TODO

#include <iostream>
#include <cstring>
using namespace std;

void copyData(char *dest, const char *src) {
    // TODO: Add bounds check
    strcpy(dest, src); // ⚠️ unsafe copy
}

int main() {
    char buffer[10];
    copyData(buffer, "This is a very long string");
    cout << "Buffer: " << buffer << endl;
    return 0;
}
