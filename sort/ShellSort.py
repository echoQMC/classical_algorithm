#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 希尔排序（插入排序改）


def shellSort(array):
    n = len(array)
    gap = int(n / 2)

    while gap > 0:

        for i in range(gap, n):
            tmp = array[i]
            j = i

            # 开始一次插入排序,step 为 gap
            while j >= gap and array[j - gap] > tmp:
                array[j] = array[j - gap]
                j -= gap

            array[j] = tmp

        gap = int(gap / 2)

    return array


if __name__ == '__main__':
    arrays = [
        [5, 2, 1, 6, 8, 2, 0, 3],
        [10, 2, -1, -6, 2, 5, 7],
        [4, 5, 0, 2, 5, 2, 5, -9]
    ]
    for array in arrays:
        print shellSort(array)
