#ifndef INTERPOLATION_SEARCH_H
#define INTERPOLATION_SEARCH_H

int interpolationSearch(double *arr, int size, int val) {
    int low = 0, high = (size - 1);
    while (low <= high && val >= arr[low] && val <= arr[high]) {
        if (low == high) {
            if (arr[low] == val) return low;
            return -1;
        }
        int pos = low + (((double)(high - low) / (arr[high] - arr[low])) * (val - arr[low]));

        if (arr[pos] == val)
            return pos;

        if (arr[pos] < val)
            low = pos + 1;

        else
            high = pos - 1;
    }
    return -1;
}

#endif  // INTERPOLATION_SEARCH_H
