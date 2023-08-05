#ifndef SHELL_SORT_H
#define SHELL_SORT_H

#include "utils.h"

void shellSort(double *arr, int len) {
    int i, j, interval;

    for (interval = len / 2; interval > 0; interval = interval / 2)
        for (i = interval; i < len; i++)
            for (j = i - interval; j >= 0 && arr[j] > arr[j + interval]; j = j - interval)
                swap(&arr[j], &arr[j + interval]);
}

#endif  // SHELL_SORT_H
