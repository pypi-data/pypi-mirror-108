#ifndef INSERTION_SORT_H
#define INSERTION_SORT_H

void insertionSort(double *arr, int size) {
    int i, j;
    double key;
    for (i = 1; i < size; i++) {
        j = i - 1;
        key = arr[i];
        while (j >= 0 && key < arr[j]) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}

#endif //INSERTION_SORT_H
