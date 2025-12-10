// Advanced C: use-after-free, double free, integer overflow
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

void use_after_free() {
    char *p = malloc(20);
    strcpy(p, "abc");
    free(p);
    printf("%s\n", p); // use after free
}

void double_free() {
    char *q = malloc(10);
    free(q);
    free(q); // double free
}

void int_overflow(int n) {
    int len = n * 1000000; // potential overflow
    char *buf = malloc(len);
    if (!buf) return;
    memset(buf, 0, len);
    free(buf);
}
