// gcc -o cpu_hog cpu_hog.c

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <seconds>\n", argv[0]);
        return 1;
    }

    int seconds = atoi(argv[1]);
    if (seconds <= 0) {
        fprintf(stderr, "Please provide a positive number of seconds.\n");
        return 1;
    }

    printf("Consuming 100%% CPU for %d seconds...\n", seconds);

    // Get the end time by adding 'seconds' to the current time
    time_t end_time = time(NULL) + seconds;


    // infinite loop
    while (time(NULL) < end_time) {
        // Empty loop to consume CPU
    }

    printf("Done.\n");
    return 0;
}