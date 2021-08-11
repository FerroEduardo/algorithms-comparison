/*
Randomised quick sort implementation in C language.
In normal quick sort, pivot chosen to partition is either the first or the last
element of the array. This can take time O(n*n) to sort in the worst case. Now
in randomised quick sort, pivot is randomly chosen and then recursively sort the
left and right sub-arrays. The expected running time of the algorithm is
O(nlog(n)).
*/
#include <iostream>
#include <string>
#include <cstdint>
#include "System.hpp"
#include "App.hpp"
using namespace std;

//esse é brabo
//g++ ./lib/System.cpp algorithms/quick_sort.cpp -o bin/quick_sort -I./lib/ -I. -lm -lpapi
//g++ algorithms/quick.cpp -S -m64 -O0
//g++ -I. -I./lib/ ./lib/System.cpp algorithms/quick_sort.cpp -lm -o bin/quick_sort.cpp

int getBig(int64_t *a, int i, int right, int pivot)
{
    for (int k = i; k <= right; k++)
    {
        if (a[k] > pivot)
            return k;
    }
    return right + 1;
}

int getSmall(int64_t *a, int j, int left, int pivot)
{
    for (int k = j; k >= left; k--)
    {
        if (a[k] < pivot)
            return k;
    }
    return -1;
}

void swap(int64_t *a, int64_t *b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

void random_quick(int64_t *a, int left, int right)
{
    if (left >= right)
        return;
    int index = left + (rand() % (right - left)), i = left, j = right;
    int pivot_index = index;
    int pivot = a[index];
    // storing index of element greater than pivot
    i = getBig(a, i, right, pivot);
    // storing index of element smaller than pivot
    j = getSmall(a, j, left, pivot);
    while (i <= j)
    {
        swap(&a[i], &a[j]);
        i = getBig(a, i, right, pivot);
        j = getSmall(a, j, left, pivot);
    }
    // after separating the smaller and greater elements, there are 3 cases
    // possible
    if (pivot_index > j && pivot_index > i)
    {
        // case 1. When the pivot element index is greater than both i and j
        swap(&a[i], &a[pivot_index]);
        random_quick(a, left, i - 1);
        random_quick(a, i + 1, right);
    }
    else if (pivot_index < j && pivot_index < i)
    {
        // case 2. When the pivot element index is smaller than both i and j
        swap(&a[j], &a[pivot_index]);
        random_quick(a, left, j - 1);
        random_quick(a, j + 1, right);
    }
    else
    {
        // the pivot element is at its origin position.
        random_quick(a, left, pivot_index - 1);
        random_quick(a, pivot_index + 1, right);
    }
}

int main(int argc, char const *argv[])
{
    /*
    argv[1] -> file to read
    argv[2] -> number of elements
    argv[3] -> processor name
    */
   
    srand(99);
    int num = atoi(argv[2]);
    uint64_t nInstr = 350;
    nInstr *= num; //Prevent overflow
    nInstr *= num; //Worst O(n*n)
    printf("Filename: %s\nSize: %d\n", argv[1], atoi(argv[2]));
    int64_t *arr;// = (int64_t *)malloc(num * sizeof(int64_t));
    posix_memalign(reinterpret_cast <void**>(&arr), 64, num * sizeof(int64_t));
    FILE *fp = fopen(argv[1], "r");
    for (int i = 0; i < num; i++)
    {
        fscanf(fp, "%ld", &arr[i]);
    }
    fclose(fp);
    Events events;
    events.setNumberOfEvents(4);
    events.addEvents(PAPI_TOT_CYC);
    events.addEvents(PAPI_REF_CYC);
    events.addEvents(PAPI_L3_TCM);
    events.addEvents(PAPI_TOT_INS);
    events.start();
    Stopwatch stopwatch;
    FREQUENCY(stopwatch);
    START_STOPWATCH(stopwatch);
    random_quick(arr, 0, num - 1);
    STOP_STOPWATCH(stopwatch);
    events.stop();
    // cout << "PAPI_TOT_CYC: " << events.getEventbyIndex(0)  << endl;
    // cout << "PAPI_REF_CYC: " << events.getEventbyIndex(1)  << endl;
    // cout << "PAPI_L3_TCM: " << events.getEventbyIndex(2)  << endl;
    double time_spent = stopwatch.mElapsedTime;
    string processor = argv[3];
    string filepath = "./results/processors/" + processor + "/result_quick_sort.txt";
    FILE *dataFile = fopen(filepath.c_str(), "a");
    fprintf(dataFile, "%d;%.10lf;%lld;%lld;%lld;%ld;%lu;%lld\n", num, time_spent, events.getEventbyIndex(0), events.getEventbyIndex(1), events.getEventbyIndex(2), num * sizeof(int64_t), nInstr, events.getEventbyIndex(3));
    fclose(dataFile);

    free(arr);
    return 0;
}