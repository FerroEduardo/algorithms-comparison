/**
 * @file
 * @author [Dhruv Pasricha](https://github.com/DhruvPasricha)
 * @brief [Heap Sort](https://en.wikipedia.org/wiki/Heapsort) implementation
 * @details
 * Heap-sort is a comparison-based sorting algorithm.
 * Heap-sort can be thought of as an improved selection sort:
 * like selection sort, heap sort divides its input into a sorted
 * and an unsorted region, and it iteratively shrinks the unsorted
 * region by extracting the largest element from it and inserting
 * it into the sorted region.
 *
 * Unlike selection sort,
 * heap sort does not waste time with a linear-time scan of the
 * unsorted region; rather, heap sort maintains the unsorted region
 * in a heap data structure to more quickly find the largest element
 * in each step.
 * Time Complexity : O(Nlog(N))
 */
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <iomanip>
#include <cassert>
#include <cstdio>
#include <climits>
#include <cstring>
#include <string>
#include <cstdint>
#include "System.hpp"
using namespace std;

/**
 * @brief Swapped two numbers using pointer
 * @param first pointer of first number
 * @param second pointer of second number
 */
void swap(int64_t *first, int64_t *second)
{
    int64_t temp = *first;
    *first = *second;
    *second = temp;
}

/**
 * @brief heapifyDown Adjusts new root to the correct position in the heap
 * This heapify procedure can be thought of as building a heap from
 * the top down by successively shifting downward to establish the
 * heap property.
 * @param arr array to be sorted
 * @param size size of array
 * @return void
*/
void heapifyDown(int64_t *arr, const int64_t size)
{
    int i = 0;

    while (2 * i + 1 < size)
    {
        int maxChild = 2 * i + 1;

        if (2 * i + 2 < size && arr[2 * i + 2] > arr[maxChild])
        {
            maxChild = 2 * i + 2;
        }

        if (arr[maxChild] > arr[i])
        {
            swap(&arr[i], &arr[maxChild]);
            i = maxChild;
        }
        else
        {
            break;
        }
    }
}

/**
 * @brief heapifyUp Adjusts arr[i] to the correct position in the heap
 * This heapify procedure can be thought of as building a heap from
 * the bottom up by successively shifting upward to establish the
 * heap property.
 * @param arr array to be sorted
 * @param i index of the pushed element
 * @return void
*/
void heapifyUp(int64_t *arr, int i)
{
    while (i > 0 && arr[i / 2] < arr[i])
    {
        swap(&arr[i / 2], &arr[i]);
        i /= 2;
    }
}

/**
 * @brief Heap Sort algorithm
 * @param arr array to be sorted
 * @param size size of the array
 * @returns void
 */
void heapSort(int64_t *arr, const int64_t size)
{
    if (size <= 1)
    {
        return;
    }

    for (int i = 0; i < size; i++)
    {
        // Pushing `arr[i]` to the heap

        /*heapifyUp Adjusts arr[i] to the correct position in the heap*/
        heapifyUp(arr, i);
    }

    for (int64_t i = size - 1; i >= 1; i--)
    {
        // Moving current root to the end
        swap(&arr[0], &arr[i]);

        // `heapifyDown` adjusts new root to the correct position in the heap
        heapifyDown(arr, i);

    }
}

/**
 * @brief Main function
 * @returns 0 on exit
 */
int main(int argc, char const *argv[])
{
    /*
    argv[1] -> file to read
    argv[2] -> number of elements
    */
    srand(time(NULL));
    int num = atoi(argv[2]);
    // printf("Filename: %s\nSize: %d\n", argv[1], atoi(argv[2]));
    int64_t *arr = (int64_t *)malloc(num * sizeof(int64_t));
    FILE *fp = fopen(argv[1], "r");
    for (int i = 0; i < num; i++)
    {
        fscanf(fp, "%ld", &arr[i]);
    }
    fclose(fp);
    Events events;
    events.setNumberOfEvents(3);
    events.addEvents(PAPI_TOT_CYC);
    events.addEvents(PAPI_REF_CYC);
    events.addEvents(PAPI_L3_TCM);
    events.start();
    clock_t begin = clock();
    heapSort(arr, num);
    clock_t end = clock();
    cout << "PAPI_TOT_CYC: " << events.getEventbyIndex(0)  << endl;
    cout << "PAPI_REF_CYC: " << events.getEventbyIndex(1)  << endl;
    cout << "PAPI_L3_TCM: " << events.getEventbyIndex(2)  << endl;
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    FILE *dataFile = fopen("./results/result_heap_sort.txt", "a");
    fprintf(dataFile, "%d;%.10lf;%lld;%lld;%lld\n", num, time_spent, events.getEventbyIndex(0), events.getEventbyIndex(1), events.getEventbyIndex(2));
    fclose(dataFile);


    free(arr);
    return 0;
}
