#ifndef MERGE_SORT_H
#define MERGE_SORT_H

#include <stdlib.h>

#include "utils.h"

void merge(double *arr, int left, int middle, int right) {
    int i, j, k;
    int n1 = middle - left + 1;
    int n2 = right - middle;
    double *Left, *Right;

    Left = (double*)malloc(n1 * sizeof(double));
    Right = (double*)malloc(n2 * sizeof(double));

    for (i = 0; i < n1; i++)
        Left[i] = arr[left + i];
    for (j = 0; j < n2; j++)
        Right[j] = arr[middle + 1 + j];

    i = 0;
    j = 0;
    k = left;
    while (i < n1 && j < n2) {
        if (Left[i] <= Right[j]) {
            arr[k] = Left[i];
            i++;
        }
        else {
            arr[k] = Right[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr[k] = Left[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = Right[j];
        j++;
        k++;
    }

    free(Left);
    free(Right);
}

void mergeSort(double *arr, int left, int right) {
    if (left < right) {
        int middle = left + (right - left) / 2;

        mergeSort(arr, left, middle);
        mergeSort(arr, middle + 1, right);

        merge(arr, left, middle, right);
    }
}

#endif // MERGE_SORT_H
