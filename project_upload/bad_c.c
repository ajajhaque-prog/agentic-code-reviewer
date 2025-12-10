// bad_c.c
// Example C file with unsafe functions

#include <stdio.h>
#include <string.h>

void greet() {
    char name[20];
    printf("Enter name: ");
    gets(name); // ⚠️ Unsafe: buffer overflow risk
    printf("Hello %s\n", name);
}

int main() {
    greet();
    return 0;
}
