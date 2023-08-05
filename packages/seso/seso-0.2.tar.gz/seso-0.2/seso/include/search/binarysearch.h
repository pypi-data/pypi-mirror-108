#ifndef BINARY_SEARCH_H
#define BINARY_SEARCH_H

int binarySearch(double *arr, int left, int right, double val) {
    int mid;
    if (right >= left) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == val)
            return mid;

        if (arr[mid] > val)
            return binarySearch(arr, left, mid - 1, val);

        return binarySearch(arr, mid + 1, right, val);
    }
    return -1;
}

#endif  // BINARY_SEARCH_H
