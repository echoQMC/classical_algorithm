#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 冒泡排序


def bubbleSort(array):
    """
    冒泡排序
    """
    n = len(array)

    for i in range(n):

        flag = False
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                array[j + 1], array[j] = array[j], array[j + 1]
                flag = True

        # 如果某一轮对比没有移动数据，说明已经是排序好了
        if flag is False:
            break

    return array


if __name__ == '__main__':
    arrays = [
        [5, 2, 1, 6, 8, 2, 0, 3],
        [10, 2, -1, -6, 2, 5, 7],
        [4, 5, 0, 2, 5, 2, 5, -9]
    ]
    for array in arrays:
        print bubbleSort(array)
