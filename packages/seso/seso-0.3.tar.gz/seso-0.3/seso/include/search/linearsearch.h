#ifndef LINEAR_SEARCH_H
#define LINERA_SEARCH_H

int linearSearch(double *arr, int size, double val)
{
    int i, ret=-1;
    for (i = 0; i < size; i++)
    {
        if (arr[i] == val)
            ret = i;
    }
    return ret;
}

#endif // LINEAR_SEARCH_H
