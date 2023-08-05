#ifndef HEAP_SORT_H
#define HEAP_SORT_H

#include "utils.h"

void heapify(double *arr, int n, int i) {
    int largest = i;
    int l = 2 * i + 1;
    int r = 2 * i + 2;
 
    if (l < n && arr[l] > arr[largest])
        largest = l;
 
    if (r < n && arr[r] > arr[largest])
        largest = r;
 
    if (largest != i) {
        swap(&arr[i], &arr[largest]);
        heapify(arr, n, largest);
    }
}

void heapSort(double *arr, int size) {
    int i, j;
    for (i = size / 2 - 1; i >= 0; i--)
        heapify(arr, size, i);
 
    for (j = size - 1; j > 0; j--) {
        swap(&arr[0], &arr[j]);
        heapify(arr, j, 0);
    }
}

#endif // HEAP_SORT_H
