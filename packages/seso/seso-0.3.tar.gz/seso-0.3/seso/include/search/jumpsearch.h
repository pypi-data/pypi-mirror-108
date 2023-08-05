#ifndef JUMP_SEARCH_H
#define JUMP_SEARCH_H

#include <math.h>

int jumpSearch(double *arr, int n, double val) {
    int step = floor(sqrt(n)), prev = 0;

    while (arr[min(step, n) - 1] < val) {
        prev = step;
        step += floor(sqrt(n));
        if (prev >= n) {
            return -1;
        }
    }

    while (arr[prev] < val) {
        prev = prev + 1;
        if (prev == min(step, n)) {
            return -1;
        }
    }
    if (arr[prev] == val) {
        return prev;
    }
    return -1;
}

#endif  // JUMP_SEARCH_H
