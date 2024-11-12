// gcc -o mem_hog mem_hog.c

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/sysinfo.h>
#include <string.h>

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

    // Obtenir la quantité totale de mémoire physique disponible
    struct sysinfo info;
    if (sysinfo(&info) != 0) {
        perror("sysinfo");
        return 1;
    }

    size_t total_mem = info.freeram; // Quantité de RAM libre
    char *memory_block;

    printf("Allocating approximately %zu MB of memory.\n", total_mem / (1024 * 1024));

    // Essayer d'allouer toute la mémoire libre
    memory_block = malloc(total_mem);
    if (memory_block == NULL) {
        perror("malloc");
        return 1;
    }

    // Fill the allocated memory with data to avoid swapping
    memset(memory_block, 0, total_mem);

    printf("Memory allocated and filled. Holding for %d seconds...\n", seconds);
    sleep(seconds);

    free(memory_block);
    printf("Memory released.\n");

    return 0;
}