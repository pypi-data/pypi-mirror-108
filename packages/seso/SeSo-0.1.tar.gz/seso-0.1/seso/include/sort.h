#ifndef SORT_H
#define SORT_H

#include "sort/bubblesort.h"
#include "sort/selectionsort.h"
#include "sort/insertionsort.h"
#include "sort/quicksort.h"
#include "sort/mergesort.h"
#include "sort/heapsort.h"
#include "sort/bucketsort.h"
#include "sort/radixsort.h"

int sort(double *arr, int len, char *algorithm) {
    if (strcmp(algorithm, "bubblesort") == 0) {
        bubbleSort(arr, len);
    } else if (strcmp(algorithm, "selectionsort") == 0) {
        selectionSort(arr, len);
    } else if (strcmp(algorithm, "insertionsort") == 0) {
        insertionSort(arr, len); 
    } else if (strcmp(algorithm, "quicksort") == 0) {
        quickSort(arr, 0, len-1); 
    } else if (strcmp(algorithm, "mergesort") == 0) {
        mergeSort(arr, 0, len-1); 
    } else if (strcmp(algorithm, "heapsort") == 0) {
        heapSort(arr, len); 
    } else if (strcmp(algorithm, "bucketsort") == 0) {
        bucketSort(arr, len); 
    } else if (strcmp(algorithm, "radixsort") == 0) {
        radixSort(arr, len); 
    } else {
        return 1;
    }
    return 0;
}

#endif //SORT_H
