#ifndef TIM_SORT_H
#define TIM_SORT_H

#include "insertionsort.h"
#include "mergesort.h"

const int RUN = 32;

void timSort(double *arr, int size) {
    int i, n, left, middle, right;
    for (i = 0; i < size; i += RUN)
        insertionSort(arr, i, min((i + RUN - 1), (size - 1)));
    for (n = RUN; n < size; n = 2 * n) {
        for (left = 0; left < size; left += 2 * n) {
            middle = left + n - 1;
            right = min((left + 2 * n - 1), (size - 1));
            if (middle < right)
                merge(arr, left, middle, right);
        }
    }
}

#endif  //TIM_SORT_H
