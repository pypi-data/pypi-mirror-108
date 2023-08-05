#ifndef SEARCH_H
#define SEARCH_H

#include "search/linearsearch.h"
#include "search/binarysearch.h"
#include "search/jumpsearch.h"
#include "search/interpolationsearch.h"
#include "search/exponentialsearch.h"
#include "search/fibonaccisearch.h"
#include "search/ternarysearch.h"

int search(double *arr, double val, int len, char* algorithm) {
    if (strcmp(algorithm, "linearsearch") == 0) {
        return linearSearch(arr, len, val);
    } else if (strcmp(algorithm, "binarysearch") == 0) {
        return binarySearch(arr, 0, len-1, val);
    } else if (strcmp(algorithm, "jumpsearch") == 0) {
        return jumpSearch(arr, len, val); 
    } else if (strcmp(algorithm, "interpolationsearch") == 0) {
        return interpolationSearch(arr, len, val); 
    } else if (strcmp(algorithm, "exponentialsearch") == 0) {
        return exponentialSearch(arr, len, val); 
    } else if (strcmp(algorithm, "fibonaccisearch") == 0) {
        return fibonacciSearch(arr, len, val); 
    } else if (strcmp(algorithm, "ternarysearch") == 0) {
        return ternarySearch(arr, 0, len-1, val); 
    } else {
        return 1;
    }
    return 0;
}

#endif // SEARCH_H
