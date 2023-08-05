#ifndef RADIX_SORT_H
#define RADIX_SORT_H

#include <stdlib.h>

double getMax(double *arr, int n) {
    double max = arr[0];
    for (int i = 1; i < n; i++)
        if (arr[i] > max)
            max = arr[i];
    return max;
}

void countSort(double *arr, int size, int exp) {
    double *output;
    int i, temp, count[10] = {0};

    output = (double*)malloc(size * sizeof(double));

    for (i = 0; i < size; i++) {
        temp = arr[i];
        count[(temp / exp) % 10]++;
    }

    for (i = 1; i < 10; i++)
        count[i] += count[i - 1];

    for (i = size - 1; i >= 0; i--) {
        temp = arr[i];
        output[count[(temp / exp) % 10] - 1] = arr[i];
        count[(temp / exp) % 10]--;
    }

    for (i = 0; i < size; i++)
        arr[i] = output[i];
}

void radixSort(double *arr, int size) {
    double m = getMax(arr, size);
    int exp;
    for (exp = 1; m / exp > 0; exp *= 10)
        countSort(arr, size, exp);
}

#endif  // RADIX_SORT_H
