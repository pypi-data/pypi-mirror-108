#ifndef FIBONACCI_SEARCH_H
#define FIBONACCI_SEARCH_H

int fibonacciSearch(double *arr,  int size, double val) {
    int fibMMm2 = 0;
    int fibMMm1 = 1;
    int fibM = fibMMm2 + fibMMm1;
    int i, offset;

    while (fibM < size) {
        fibMMm2 = fibMMm1;
        fibMMm1 = fibM;
        fibM = fibMMm2 + fibMMm1;
    }

    offset = -1;

    while (fibM > 1) {
        i = ((offset + fibMMm2) < (size - 1)) ? (offset + fibMMm2) : (size - 1);

        if (arr[i] < val) {
            fibM = fibMMm1;
            fibMMm1 = fibMMm2;
            fibMMm2 = fibM - fibMMm1;
            offset = i;
        }

        else if (arr[i] > val) {
            fibM = fibMMm2;
            fibMMm1 = fibMMm1 - fibMMm2;
            fibMMm2 = fibM - fibMMm1;
        }

        else
            return i;
    }

    if (fibMMm1 && arr[offset + 1] == val)
        return offset + 1;

    return -1;
}

#endif  // FIBONACCI_SEARCH_H
