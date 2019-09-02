#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 插入排序


def insertSort(array):
    n = len(array)

    if n <= 1:
        return array

    for i in range(1, n):
        tmp_val = array[i]

        # 查找合适的插入位置(注意 j 可以为 -1)
        for j in range(i - 1, -2, -1):
            if array[j] > tmp_val:
                array[j + 1] = array[j]   # 数据移动
            else:
                break

        array[j + 1] = tmp_val

    return array


if __name__ == '__main__':
    arrays = [
        [5, 2, 1, 6, 8, 2, 0, 3],
        [10, 2, -1, -6, 2, 5, 7],
        [4, 5, 0, 2, 5, 2, 5, -9]
    ]
    for array in arrays:
        print insertSort(array)
