# SeSo documentation

## Search Algorithms

<br/>

| Algorithm             |  Code                     | Time Complexity   |
|-----------------------|---------------------------|-------------------|
| Linear Search         | linearsearch              | O(n)              |
| Binary Search         | binarysearch              | O(logn)           |
| Jump Search           | jumpsearch                | O(√n)             |
| Interpolation Search  | interpolationsearch       | O(n)              |
| Exponential Search    | exponentialsearch         | O(Log n)          |
| Fibonacci Search      | fibonaccisearch           | O(Log n)          |
| Ternary Search        | ternarysearch             | O(log3 n)         |

<br/>

## ```seso.search(a, value, algorithm={code})```

<br/>

**Returns index of the element if found, else -1.**

- **Parameters**
    - **a** : array to be sorted.
    - **value** : value to be searched.
    - **Algorithm** (optional) : Searching algorithm. The default is bubblesort.

- **Returns**
    - The index if value found, else -1.

### Example

```python
import seso

seso.search([1,4,2,5,7], 4, 'jumpsearch')
```
<br/>

## Sort Algorithms

<br/>

| Algorithm             |  Code                     | Time Complexity   |
|-----------------------|---------------------------|-------------------|
| Bubble Sort           | bubblesort                | O(n^2)            |
| selection Sort        | selectionsort             | O(n^2)            |
| Insertion Sort        | Insertion Sort            | O(n^2)            |
| Merge Sort            | mergesort                 | O(n log(n))       |
| Quick Sort            | quicksort                 | O(n^2)            |
| Heap Sort             | heapsort                  | O(n log(n))       |
| Radix Sort            | radixsort                 | O(nk)             |
| Bucket Sort           | bucketsort                | O(n^2)            |
| Shell Sort            | shellsort                 | O(n log(n))       |
| Tim Sort              | timsort                   | O(n log(n))       |

<br/>

## ```seso.sort(a, algorithm={code})```

<br/>

**Returns a sorted copy of an array.**

- **Parameters**
    - **a** : array to be sorted.
    - **Algorithm** (optional) : Sorting algorithm. The default is mergesort.

- **Returns**
    - sorted array.

### Example

```python
import seso

seso.sort([1,4,2,5,4], 'quicksort')
```

*Note: Time Complexities are worst case time complexities (Big O)*
