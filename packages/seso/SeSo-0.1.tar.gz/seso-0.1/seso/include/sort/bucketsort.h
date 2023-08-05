#ifndef BUCKET_SORT_H
#define BUCKET_SORT_H

void bucketSort(double *arr, int size) {
    int i, j, temp;
    int *count;

    count = (int*)malloc(size * sizeof(int));

    for (i = 0; i < size; i++)
        count[i] = 0;

    for (i = 0; i < size; i++) {
        temp = arr[i];
        (count[temp])++;
    }

    for (i = 0, j = 0; i < size; i++)
        for (; count[i] > 0; (count[i])--)
            arr[j++] = i;
    
    free(count);
}

#endif  // BUCKET_SORT_H
