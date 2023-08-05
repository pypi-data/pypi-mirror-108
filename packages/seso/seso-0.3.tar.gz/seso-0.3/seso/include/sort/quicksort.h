#ifndef QUICK_SORT_H
#define QUICK_SORT_H

#include "utils.h"

int partition(double *arr, int lower, int upper) {
    int i, j;
    double pivot;
    i = (lower - 1);
    pivot = arr[upper];
    for (j = lower; j < upper; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[upper]);
    return (i + 1);
}

void quickSort(double *arr, int lower, int upper) {   
    int partitionIndex;
    if (upper > lower) {
        partitionIndex = partition(arr, lower, upper);
        quickSort(arr, lower, partitionIndex - 1);
        quickSort(arr, partitionIndex + 1, upper);
    }
}

#endif //QUICK_SORT_H
