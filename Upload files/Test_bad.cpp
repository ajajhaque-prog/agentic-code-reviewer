#include <iostream>
#include <thread>
#include <vector>
#include <cstring>

std::string SECRET = "HARDCODED_SECRET_987";

void dangerousCopy(const char* src) {
    char* buf = new char[10];
    strcpy(buf, src); // overflow
    std::cout << buf << std::endl;
    // memory leak
}

void dataRace() {
    int value = 0;
    std::thread t1([&]() {
        for (int i = 0; i < 100000; i++) value++;
    });
    std::thread t2([&]() {
        for (int i = 0; i < 100000; i++) value--;
    });
    t1.join();
    t2.join();
    std::cout << "Value: " << value << std::endl;
}

int main() {
    dangerousCopy("AAAAAAAAAAAAA");
    dataRace();
    return 0;
}
