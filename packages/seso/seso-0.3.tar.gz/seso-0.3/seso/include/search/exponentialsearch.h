#ifndef EXPONENTIAL_SEARCH_H
#define EXPONENTIAL_SEARCH_H

int binary_search(double *arr, int l_index, int r_index, double n) {
    int middle_index = l_index + (r_index - l_index) / 2;
    if (l_index > r_index) {
        return -1;
    }
    if (arr[middle_index] == n) {
        return middle_index;
    }
    if (arr[middle_index] > n) {
        return binary_search(arr, l_index, middle_index - 1, n);
    }
    return binary_search(arr, middle_index + 1, r_index, n);
}

int exponentialSearch(double *arr, int size, double val) {
    if (size == 0) {
        return -1;
    }
    int upper_bound = 1, lower_bound;
    while (upper_bound <= size && arr[upper_bound] < val) {
        upper_bound = upper_bound * 2;
    }
    lower_bound = upper_bound / 2;
    if (upper_bound > size) {
        upper_bound = size;
    }
    return binary_search(arr, lower_bound, upper_bound, val);
}

#endif  // EXPONENTIAL_SEARCH_H
