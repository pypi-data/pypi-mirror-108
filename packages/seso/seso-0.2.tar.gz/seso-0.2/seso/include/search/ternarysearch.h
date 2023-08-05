#ifndef TERNARY_SEARCH_H
#define TERNARY_SEARCH_H

int ternarySearch(double *arr, int left, int right, int val) {
    int mid1, mid2;
    if (right >= left) {
        mid1 = left + (right - left) / 3;
        mid2 = right - (right - left) / 3;

        if (arr[mid1] == val) {
            return mid1;
        }
        if (arr[mid2] == val) {
            return mid2;
        }

        if (val < arr[mid1]) {
            return ternarySearch(arr, left, mid1 - 1, val);
        } else if (val > arr[mid2]) {
            return ternarySearch(arr, mid2 + 1, right, val);
        } else {
            return ternarySearch(arr, mid1 + 1, mid2 - 1, val);
        }
    }

    return -1;
}

#endif  // TERNARY_SEARCH_H
