/**
 * @file
 * @brief Implementation of [merge
 * sort](https://en.wikipedia.org/wiki/Merge_sort) algorithm
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
 * @addtogroup sorting Sorting algorithms
 * @{
 */
/** Swap two integer variables
 * @param [in,out] a pointer to first variable
 * @param [in,out] b pointer to second variable
 */
void swap(int64_t *a, int64_t *b)
{
    int t;
    t = *a;
    *a = *b;
    *b = t;
}

/**
 * @brief Perform merge of segments.
 *
 * @param a array to sort
 * @param l left index for merge
 * @param r right index for merge
 * @param n total number of elements in the array
 */
void merge(int64_t *a, int l, int r, int n)
{
    int64_t *b = (int64_t *)malloc(n * sizeof(int64_t)); /* dynamic memory must be freed */
    int c = l;
    int p1, p2;
    p1 = l;
    p2 = ((l + r) / 2) + 1;
    while ((p1 < ((l + r) / 2) + 1) && (p2 < r + 1))
    {
        if (a[p1] <= a[p2])
        {
            b[c++] = a[p1];
            p1++;
        }
        else
        {
            b[c++] = a[p2];
            p2++;
        }
    }

    if (p2 == r + 1)
    {
        while ((p1 < ((l + r) / 2) + 1))
        {
            b[c++] = a[p1];
            p1++;
        }
    }
    else
    {
        while ((p2 < r + 1))
        {
            b[c++] = a[p2];
            p2++;
        }
    }

    for (c = l; c < r - l + 1; c++) a[c] = b[c];

    free(b);
}

/** Merge sort algorithm implementation
 * @param a array to sort
 * @param n number of elements in the array
 * @param l index to sort from
 * @param r index to sort till
 */
void merge_sort(int64_t *a, int n, int l, int r)
{
    if (r - l == 1)
    {
        if (a[l] > a[r])
            swap(&a[l], &a[r]);
    }
    else if (l != r)
    {
        merge_sort(a, n, l, (l + r) / 2);
        merge_sort(a, n, ((l + r) / 2) + 1, r);
        merge(a, l, r, n);
    }

    /* no change if l == r */
}
/** @} */

/** Main function */
int main(int argc, char const *argv[])
{
    /*
    argv[1] -> file to read
    argv[2] -> number of elements
    */
    int num = atoi(argv[2]);
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
    merge_sort(arr, num, 0, num - 1);
    clock_t end = clock();
    events.stop();
    cout << "PAPI_TOT_CYC: " << events.getEventbyIndex(0)  << endl;
    cout << "PAPI_REF_CYC: " << events.getEventbyIndex(1)  << endl;
    cout << "PAPI_L3_TCM: " << events.getEventbyIndex(2)  << endl;
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    FILE *dataFile = fopen("./results/result_merge_sort.txt", "a");
    fprintf(dataFile, "%d;%.10lf;%lld;%lld;%lld\n", num, time_spent, events.getEventbyIndex(0), events.getEventbyIndex(1), events.getEventbyIndex(2));
    fclose(dataFile);

    free(arr);
    return 0;
}
