#include <stdio.h>
#include <stdlib.h>

// gcc -o cpu_hog_load cpu_hog_load.c


int main(int argc, char *argv[]) {
    unsigned long long loop_size = 0;

    if (argc > 1) {
        loop_size = strtoull(argv[1], NULL, 10);
        printf("Running with loop size: %llu\n", loop_size);
    } else {
        printf("Running in infinite loop (press Ctrl+C to stop)\n");
    }

    unsigned long long i = 0;

    if (loop_size > 0) {
        for (i = 0; i < loop_size; i++) {
        }
        printf("Loop completed\n");
    } else {
        while (1) {
  
        }
    }

    return 0;
}
