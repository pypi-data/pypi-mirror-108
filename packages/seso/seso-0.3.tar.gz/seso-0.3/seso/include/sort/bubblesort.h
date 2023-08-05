#ifndef BUBBLE_SORT_H
#define BUBBLE_SORT_H

#include "utils.h"

void bubbleSort(double *arr, int size) {
    int flag;
    for (int i = 0; i < size - 1; i++) {
        flag = 0;
        for (int j = 0; j < size - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {
                swap(&arr[j], &arr[j + 1]);
                flag = 1;
            }
        }
        if (!flag) {
            break;
        }
    }
}

#endif  //BUBBLE_SORT_H
