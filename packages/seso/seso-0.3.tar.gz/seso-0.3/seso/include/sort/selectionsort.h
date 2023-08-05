#ifndef SELECTION_SORT_H
#define SELECTION_SORT_H

#include "utils.h"

void selectionSort(double *arr, int size) {
    int i, j, min_index;
    for (i = 0; i < size - 1; i++)
    {
        min_index = i;
        for (j = i + 1; j < size; j++) {
            if (arr[min_index] > arr[j]) {
                min_index = j;
            }
        }
        if (min_index != i) {
            swap(arr + i, arr + min_index);
        }
    }
}

#endif //SELECTION_SORT_H
