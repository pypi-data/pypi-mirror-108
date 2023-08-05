#ifndef INSERTION_SORT_H
#define INSERTION_SORT_H

void insertionSort(double *arr, int left, int right) {
    int i, j;
    double key;
    for (i = left + 1; i <= right; i++) {
        j = i - 1;
        key = arr[i];
        while (j >= left && key < arr[j]) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

#endif //INSERTION_SORT_H
